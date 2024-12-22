import locale
from datetime import datetime
import polars as pl

from lanz_mining.database import mappings


# *** Assertation functions ***


def assert_column_exists(df: pl.DataFrame, columns: list[str]) -> None:
    assert all([col in df.columns for col in columns])


# *** Utility functions ***


def find_party_membership(name: str, d: datetime) -> str or None:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    membership = None
    if name in mappings.PARTY_MEMBERSHIP_MAP.keys():
        membership = mappings.PARTY_MEMBERSHIP_MAP[name]
    elif name not in mappings.PARTY_MEMBERSHIP_MAP.keys():
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
    for genre, fn in mappings.ROLE_GENRE_MAP.items():
        if isinstance(role, str) and fn(role):
            return genre
    return opt_out


def find_news_paper_affiliation(row: dict) -> str or None:
    """Looks for the role and message to find a news paper affiliation"""

    def check_row(r) -> bool:
        return all([key in r for key in ["role", "message"]])

    assert check_row(row), "Expected row to have 'role' and 'message'"
    _role = row["role"].lower()
    _message = row["message"].lower()
    default_affiliation = None
    for news_paper_name, indicators in mappings.NEWS_PAPER_MAP.items():
        is_news_paper = any(
            [(indicator in _role or indicator in _message) for indicator in indicators]
        )
        if is_news_paper:
            return news_paper_name
    return default_affiliation


# *** Pre-processing functions ***


def fix_date_col(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["lanzepisode_name"])
    locale.setlocale(locale.LC_ALL, "de_DE")
    return df.with_columns(
        date=pl.col("lanzepisode_name").map_elements(
            lambda lanzepisode_name: datetime.strptime(
                lanzepisode_name.strip("Markus Lanz vom").strip().replace(".", ""),
                "%d %B %Y",
            ),
            return_dtype=pl.Datetime,
        ),
    )


def fix_guest_names(df: pl.DataFrame) -> pl.DataFrame:
    # Normalizes ambiguous names
    def map_task(name) -> str:
        return mappings.MANUAL_NAME_MAP[name] if name in mappings.MANUAL_NAME_MAP.keys() else name

    assert_column_exists(df, ["name"])
    return df.with_columns(name=pl.col("name").map_elements(lambda n: map_task(n), pl.String))


def apply_policial_membership(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["date"])
    assert df["date"].dtype == pl.Datetime, "Function expects 'date' column of type pl.Datetime"
    political_party = df[["name", "date"]].map_rows(lambda nd: find_party_membership(nd[0], nd[1]))
    return df.insert_column(-1, pl.Series("party", political_party))


def apply_genre_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["role"])
    opt_out = "Other"
    return df.with_columns(
        genre=pl.col("role").map_elements(lambda r: find_role_genre(r, opt_out), pl.String)
    )


def apply_news_paper_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    assert_column_exists(df, ["role", "message"])
    return df.with_columns(
        pl.struct("role", "message")
        .map_elements(find_news_paper_affiliation, return_dtype=pl.String)
        .alias("news_paper")
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
    return apply_news_paper_affiliation(
        apply_genre_affiliation(apply_policial_membership(fix_guest_names(fix_date_col(df))))
    )
