import locale
from datetime import datetime

import pandas as pd
from pandas import Timestamp

from lanz_mining.database import mappings


def find_party_membership(name: str, d: Timestamp) -> str or None:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    membership = None
    if name in mappings.party_membership_map.keys():
        membership = mappings.party_membership_map[name]
    elif name not in mappings.party_membership_map.keys():
        compilcated_membership_map = mappings.get_complicated_party_memberships()
        if name in compilcated_membership_map.keys():
            membership_ranges = compilcated_membership_map[name]
            for start, end, party in membership_ranges:
                start = datetime.strptime(start, "%Y-%m-%d")
                end = datetime.strptime(end, "%Y-%m-%d")
                if start <= d < end:
                    membership = party
                    break
    return membership


def find_role_genre(role: str, opt_out: str = "Other") -> str or None:
    """Find the roles genre, applies the mapping or returns Other/None"""
    for genre, fn in mappings.role_genre_map.items():
        if isinstance(role, str) and fn(role):
            return genre
    return opt_out


def find_main_genre(df: pd.DataFrame) -> dict[str, str]:
    """Looks for role genres and maps the main role by the most often occuring."""
    name2main = {name: group["guest_genre"].max() for name, group in df.groupby("name")}
    return name2main


def repair_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Fix the dat,e column so it provides a unique date striped from the name."""
    locale.setlocale(locale.LC_ALL, "de_DE")
    df["date"] = [
        datetime.strptime(d.strip("Markus Lanz vom").strip().replace(".", ""), "%d %B %Y")
        for d in df["lanzepisode_name"].values
    ]
    return df


def fill_empty_roles(df: pd.DataFrame) -> pd.DataFrame:
    """Fixing role entries where no role is present in the raw data."""
    roles = df["role"].values
    for i, name in enumerate(df["name"].values):
        if name in mappings.manual_roles_map.keys():
            roles[i] = mappings.manual_roles_map[name]
    df["role"] = roles
    return df


def normalize_names(df: pd.DataFrame) -> pd.DataFrame:
    """Fix the names column for persons with low entropy."""
    for i, name in enumerate(df["name"].values):
        if name in mappings.manual_name_map.keys():
            df.loc[i, "name"] = mappings.manual_name_map[name]
    return df


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Remove date column, repair date data type, map party membership and guest genre."""
    del df["date"]  # date refers to publishing date and is not useful
    df = repair_date_column(df)
    df = fill_empty_roles(df)
    df = normalize_names(df)
    df["party_membership"] = [
        find_party_membership(name, d) for name, d in df[["name", "date"]].values.tolist()
    ]
    df["guest_genre"] = [find_role_genre(role) for role in df["role"].values.tolist()]
    main_genre_map = find_main_genre(df)
    df["main_genre"] = [main_genre_map[name] for name in df["name"].values.tolist()]
    return df


def preprocess_texts(df: pd.DataFrame) -> pd.DataFrame:
    """."""
    import re

    def remove_characters(text):
        characters = [".", ",", ":", ";", '"', "'", "`", "*", "&", "-"]
        pattern = "[" + re.escape("".join(characters)) + "]"
        return re.sub(pattern, " ", text).strip().lower()

    df["message"] = list(map(lambda t: remove_characters(t), df.message.values))
    return df
