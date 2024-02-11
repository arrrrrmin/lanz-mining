import locale
from datetime import datetime

import pandas as pd
from pandas import Timestamp

from lanz_mining.database.mappings import (
    party_membership_map,
    get_complicated_party_memberships,
    role_genre_map,
)


def find_party_membership(name: str, d: Timestamp) -> str or None:
    membership = None
    if name in party_membership_map.keys():
        membership = party_membership_map[name]
    elif not name in party_membership_map.keys():
        compilcated_membership_map = get_complicated_party_memberships()
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
    for genre, fn in role_genre_map.items():
        if isinstance(role, str) and fn(role):
            return genre
    return opt_out


def repair_date_column(df: pd.DataFrame):
    locale.setlocale(locale.LC_ALL, "de_DE")
    df["date"] = [
        datetime.strptime(d.strip("Markus Lanz vom").strip().replace(".", ""), "%d %B %Y")
        for d in df["lanzepisode_name"].values
    ]
    return df


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # date_convert = lambda datestr: datetime.strptime(datestr, "%Y-%m-%d")
    party_convert = lambda name, d: find_party_membership(name, d)

    del df["date"]  # date refers to publishing date and is not useful
    df = repair_date_column(df)
    df["party_membership"] = [
        party_convert(name, d) for name, d in df[["name", "date"]].values.tolist()
    ]
    df["guest_genre"] = [find_role_genre(role) for role in df["role"].values.tolist()]
    return df
