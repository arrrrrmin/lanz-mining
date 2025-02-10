import re
from datetime import datetime
from typing import Optional

import polars as pl

from lanz_mining.database import mappings
from lanz_mining.dataproc.mappings import politics
from lanz_mining.dataproc.mappings.media import MEDIA_MAPS
from lanz_mining.dataproc.mappings.roles import GROUP_MAPS, Group
from lanz_mining.dataproc.utils import requires_columns, requires_keys


KNOWN_POLITICIANS = politics.get_known_politicians()


# *** Assertation functions ***


def assert_column_exists(df: pl.DataFrame, columns: list[str]) -> None:
    assert all([col in df.columns for col in columns])


# *** Utility functions ***


def normalize_name_str(name: str) -> str:
    result_str = re.sub(",(.+)*", "", name)
    result_str = re.sub("\((.+)", "", result_str)
    result_str = result_str.replace(".", " ")
    result_str = result_str.replace("-", " ")
    result_str = result_str.replace("  ", " ")
    return result_str


def convert_factcheck_column(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(factcheck=(pl.col("factcheck") == "t"))


def convert_date_column(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(pl.col("date").str.to_datetime("%Y-%m-%d").alias("date"))


def norm_str_columns(df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
    def text_cleaner(text: str) -> str:
        return re.sub(r"„(.+)“", r'"\g<1>"', text)

    for col_name in columns:
        df = df.with_columns(
            pl.col(col_name).map_elements(lambda x: text_cleaner(x), pl.String).alias(col_name)
        )
    return df


@requires_columns("name")
def norm_names(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(name=pl.col("name").map_elements(normalize_name_str, pl.String))


def find_party_membership(row: dict) -> Optional[str]:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    name = row["name"]
    d = row["date"]

    membership = None
    if name not in KNOWN_POLITICIANS:
        return membership
    if name in politics.PARTY_MEMBERSHIP_MAP.keys():
        membership = politics.PARTY_MEMBERSHIP_MAP[name]
    else:
        compilcated_membership_map = politics.get_complicated_party_memberships()
        if name in compilcated_membership_map.keys():
            membership_ranges = compilcated_membership_map[name]
            for start, end, party in membership_ranges:
                start = datetime.strptime(start, "%Y-%m-%d").date()
                end = datetime.strptime(end, "%Y-%m-%d").date()
                if start <= d < end:
                    membership = party
                    break

    return membership


# @DeprecationWarning
@requires_keys(["role", "message", "group"])
def find_media_institute(row: dict) -> Optional[str]:
    """Looks for the role and message to find a news paper affiliation"""
    role = row["role"].lower()
    message = row["message"].lower() if row["message"] is not None else None
    group = row["group"]

    if group != "Journalismus":
        return None
    for pub_name, kw_pattern in MEDIA_MAPS.items():
        role_match = re.match(kw_pattern, role.lower()) is not None
        message_match = re.match(kw_pattern, message.lower()) is not None
        if role_match or message_match:
            return pub_name
    return None


@requires_keys(["role", "genre"])
def find_pub_platform_by_role(row: dict) -> Optional[str]:
    _role, _genre = row["role"].lower(), row["genre"]
    if _genre != "Journalismus":
        return None
    for pub_name, indicators in mappings.PUB_PLATFORM_MAP.items():
        is_platform = any([(ind in _role) for ind in indicators])
        if is_platform:
            return pub_name
    return None


# *** Pre-processing functions ***


@requires_columns("name")
def norm_abbreviated_names(df: pl.DataFrame) -> pl.DataFrame:
    # Normalizes ambiguous names
    def map_task(name) -> str:
        return (
            mappings.MANUAL_NAME_MAP[name.strip()]
            if name in mappings.MANUAL_NAME_MAP.keys()
            else name
        )

    return df.with_columns(name=pl.col("name").map_elements(lambda n: map_task(n), pl.String))


@requires_columns(["name", "date"])
def apply_policial_membership(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.struct("name", "date")
        .map_elements(find_party_membership, return_dtype=pl.String)
        .alias("party")
    )


@requires_columns(["role", "party"])
def apply_group_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    def map_fn(row: dict) -> Optional[str]:
        role, party = row["role"], row["party"]
        if party:
            return Group.Politics
        if not role:
            return None
        for group_name, kw_pattern in GROUP_MAPS.items():
            match = re.search(kw_pattern, role.lower())
            if match is not None:
                return group_name
        return Group.OptOut

    return df.with_columns(
        pl.struct("role", "party").map_elements(lambda row: map_fn(row), pl.String).alias("group")
    )


@requires_columns(["role", "message", "group"])
def apply_media_institute(df: pl.DataFrame) -> pl.DataFrame:
    def map_fn(row: dict) -> Optional[str]:
        """Looks for the role and message to find a news paper affiliation"""
        role = row["role"] if row["role"] is not None else ""
        message = row["message"] if row["message"] is not None else ""
        group = row["group"]

        if group != Group.Journalist:
            return None
        for media_name, kw_pattern in MEDIA_MAPS.items():
            print(kw_pattern)
            role_match = re.search(kw_pattern, role.lower())
            message_match = re.search(kw_pattern, message.lower())
            if role_match is not None or message_match is not None:
                return media_name
        return None

    return df.with_columns(
        pl.struct("role", "message", "group")
        .map_elements(map_fn, return_dtype=pl.String)
        .alias("media")
    )


def apply_main_genre(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["name"])
    name2main = {}
    for name, group in df.group_by("name"):
        values = group["genre"].value_counts().sort("count", descending=True)
        name2main[name[0]] = values["genre"][0]
    return df.with_columns(main_genre=pl.col("name").replace_strict(name2main))
