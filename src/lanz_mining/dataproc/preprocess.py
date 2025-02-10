import re
from datetime import datetime
from typing import Optional

import polars as pl

from lanz_mining.dataproc.mappings import politics, media, roles, types
from lanz_mining.dataproc.utils import requires_columns


KNOWN_POLITICIANS = politics.get_known_politicians()


def normalize_name_str(name: str) -> str:
    """Makes strings of name column more uniform."""
    result_str = re.sub(",(.+)*", "", name)
    result_str = re.sub("\((.+)", "", result_str)
    result_str = result_str.replace(".", " ")
    result_str = result_str.replace("-", " ")
    result_str = result_str.replace("  ", " ")
    return result_str.strip()


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
            return types.Group.Politics
        if not role:
            return None
        for group_name, kw_pattern in roles.GROUP_MAPS.items():
            match = re.search(kw_pattern, role.lower())
            if match is not None:
                return group_name
        return types.Group.OptOut

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

        if group != types.Group.Journalist:
            return None
        for media_name, kw_pattern in media.MEDIA_MAPS.items():
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


def known_groups_by_names(dataframe: pl.DataFrame) -> dict[str, Optional[str]]:
    name2main = {}
    for name, group in dataframe.group_by("name"):
        name: str = name[0]
        values = (
            group["group"]
            .value_counts()
            .sort("count", descending=True)
            .drop_nulls()["group"]
            .to_numpy()
        )
        # Implicite None only for names without any group assignment at all
        if len(values) > 0:
            name2main[name] = values[0]
    return name2main


@requires_columns(["name", "group"])
def apply_nearest_group(df: pl.DataFrame) -> pl.DataFrame:

    def map_fn(row: dict, lookup: dict[str, str]) -> Optional[str]:
        group = row["group"]
        if not group and row["name"] in lookup.keys():
            group = lookup[row["name"]]
        return group

    name2group = known_groups_by_names(df)
    return df.with_columns(
        pl.struct("name", "group")
        .map_elements(lambda row: map_fn(row, name2group), pl.String)
        .alias("group")
    )
