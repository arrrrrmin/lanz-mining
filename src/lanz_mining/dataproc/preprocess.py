import locale
import re
from datetime import datetime
from typing import Optional

import polars as pl

from lanz_mining.database import mappings
from lanz_mining.database.mappings import OTHER_GENRE_NAME
from lanz_mining.dataproc.utils import requires_columns, requires_keys


# *** Assertation functions ***


def assert_column_exists(df: pl.DataFrame, columns: list[str]) -> None:
    assert all([col in df.columns for col in columns])


# *** Utility functions ***


def convert_factcheck_column(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(factcheck=(pl.col("factcheck") == "t"))


def convert_date_column(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col("date").str.to_datetime("%Y-%m-%d").alias("date")
    )


def norm_str_columns(df: pl.DataFrame, columns: list[str]) -> pl.DataFrame:
    def text_cleaner(text: str) -> str:
        return re.sub(r"„(.+)“", r'"\g<1>"', text)

    for col_name in columns:
        df = df.with_columns(
            pl.col(col_name)
            .map_elements(lambda x: text_cleaner(x), pl.String)
            .alias(col_name)
        )
    return df


@requires_columns("name")
def norm_names(df: pl.DataFrame) -> pl.DataFrame:
    def __norm(line: str) -> str:
        line = re.sub(r"(\(.+\))", "", line)
        line = re.sub(r", (.+)", "", line)
        return line.strip()

    return df.with_columns(pl.col("name").map_elements(__norm, pl.String))


def norm_quote_marks(text: str) -> str:
    return_text = re.sub(r"„(.+)“", r'"\g<1>"', text)
    return return_text


def find_party_membership(row: dict) -> Optional[str]:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    name = row["name"]
    d = row["date"]
    membership = None
    if name in mappings.PARTY_MEMBERSHIP_MAP.keys():
        membership = mappings.PARTY_MEMBERSHIP_MAP[name]
    elif name not in mappings.PARTY_MEMBERSHIP_MAP.keys():
        compilcated_membership_map = (
            mappings.get_complicated_party_memberships()
        )
        if name in compilcated_membership_map.keys():
            membership_ranges = compilcated_membership_map[name]
            for start, end, party in membership_ranges:
                start = datetime.strptime(start, "%Y-%m-%d")
                end = datetime.strptime(end, "%Y-%m-%d")
                if start <= d < end:
                    membership = party
                    break
    return membership


def find_role_genre(
    role: str, opt_out: str = OTHER_GENRE_NAME
) -> Optional[str]:
    """Find the roles genre, applies the mapping or returns Other/None"""
    for genre, fn in mappings.ROLE_GENRE_MAP.items():
        if isinstance(role, str) and fn(role):
            return genre
    return opt_out


@requires_keys(["role", "party"])
def find_genre_by_role_party(row: dict) -> Optional[str]:
    """Tries to find a genre by looking at party and role columns."""
    role, party = row["role"], row["party"]
    if party:
        return "Politik"
    return find_role_genre(role)  # defaults to mappings.OTHER_GENRE_NAME


@requires_keys(["role", "message", "genre"])
def find_pub_platform_by_role_messsage(row: dict) -> Optional[str]:
    """Looks for the role and message to find a news paper affiliation"""
    _role = row["role"].lower()
    _message = row["message"].lower()
    _genre = row["genre"]
    if _genre != "Journalismus":
        return None
    for pub_name, indicators in mappings.PUB_PLATFORM_MAP.items():
        is_platform = any(
            [
                (indicator in _role or indicator in _message)
                for indicator in indicators
            ]
        )
        if is_platform:
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


@requires_columns("lanzepisode_name")
def fix_date_col_by_title(df: pl.DataFrame) -> pl.DataFrame:
    locale.setlocale(locale.LC_ALL, "de_DE")
    return df.with_columns(
        date=pl.col("lanzepisode_name").map_elements(
            lambda lanzepisode_name: datetime.strptime(
                lanzepisode_name.strip("Markus Lanz vom")
                .strip()
                .replace(".", ""),
                "%d %B %Y",
            ),
            return_dtype=pl.Datetime,
        ),
    )


@requires_columns("name")
def norm_abbreviated_names(df: pl.DataFrame) -> pl.DataFrame:
    # Normalizes ambiguous names
    def map_task(name) -> str:
        return (
            mappings.MANUAL_NAME_MAP[name]
            if name in mappings.MANUAL_NAME_MAP.keys()
            else name
        )

    return df.with_columns(
        name=pl.col("name").map_elements(lambda n: map_task(n), pl.String)
    )


@requires_columns(["name", "date"])
def apply_policial_membership(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.struct(pl.all())
        .map_elements(find_party_membership, return_dtype=pl.String)
        .alias("party")
    )


@requires_columns("role")
def apply_genre_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        genre=pl.col("role").map_elements(
            lambda r: find_role_genre(
                r,
                OTHER_GENRE_NAME,
            ),
            pl.String,
        )
    )


@requires_columns(["role", "genre", "message"])
def apply_pub_platform(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.struct("role", "genre", "message")
        .map_elements(
            find_pub_platform_by_role_messsage, return_dtype=pl.String
        )
        .alias("pub_platform")
    )


def apply_main_genre(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["name"])
    name2main = {}
    for name, group in df.group_by("name"):
        values = group["genre"].value_counts().sort("count", descending=True)
        name2main[name[0]] = values["genre"][0]
    return df.with_columns(main_genre=pl.col("name").replace_strict(name2main))


def default_preprocessing(df: pl.DataFrame) -> pl.DataFrame:
    # This could be more elegant?
    return apply_pub_platform(
        apply_genre_affiliation(
            apply_policial_membership(
                norm_abbreviated_names(fix_date_col_by_title(df))
            )
        )
    )
