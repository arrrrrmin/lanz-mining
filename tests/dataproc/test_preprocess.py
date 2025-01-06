import datetime

import polars as pl
from _pytest.fixtures import fixture

from lanz_mining.database import mappings
from lanz_mining.database.mappings import OTHER_GENRE_NAME
from lanz_mining.database.naming import Party
from lanz_mining.dataproc import preprocess


@fixture
def dataframe() -> pl.DataFrame:
    return pl.read_csv("tests/data/guests.csv", separator=",")


def test_fix_date_col(dataframe: pl.DataFrame):
    _df = preprocess.fix_date_col(dataframe)
    assert "date" in _df.columns
    assert _df["date"].dtype == pl.Datetime(time_unit="us", time_zone=None)
    assert len(_df) == len(dataframe)


def test_fix_guest_names(dataframe: pl.DataFrame):
    _df = preprocess.fix_guest_names(dataframe)
    assert "name" in _df.columns
    assert len(_df.filter(pl.col("name").str.contains("Madsen"))) > 0
    assert len(_df.filter(pl.col("name").str.contains("M.-A. Strack-Zimmermann"))) > 0
    assert len(_df.filter(pl.col("name").str.contains("M.- A. Strack-Zimmermann"))) == 0
    assert len(_df.filter(pl.col("name").is_null())) == 0


def test_apply_policial_membership(dataframe: pl.DataFrame):
    def check_all_mapped(name: str, party: str) -> bool:
        return all(_df.filter(pl.col("name") == name)["party"] == party)  # noqa

    _df = preprocess.fix_date_col(dataframe)
    _df = preprocess.apply_policial_membership(_df)
    assert "party" in _df.columns
    assert check_all_mapped("Cem Özdemir", Party.B90G)
    assert check_all_mapped("Wolfgang Kubicki", Party.FDP)
    assert check_all_mapped("Markus Söder", Party.CSU)
    assert check_all_mapped("Friedrich Merz", Party.CDU)
    assert not check_all_mapped("Boris Palmer", Party.B90G)
    s, e = datetime.datetime(1972, 1, 1), datetime.datetime(2023, 5, 1)
    __df = _df.filter(pl.col("date").is_between(s, e))
    assert all(__df.filter(pl.col("name").str.contains("Boris Palmer"))["party"] == Party.B90G)
    s, e = datetime.datetime(2023, 5, 1), datetime.datetime.today()
    __df = _df.filter(pl.col("date").is_between(s, e))
    assert all(__df.filter(pl.col("name").str.contains("Boris Palmer"))["party"] == Party.NP)


def test_apply_genre_affiliation(dataframe: pl.DataFrame):
    _df = preprocess.apply_genre_affiliation(dataframe)
    assert "genre" in _df.columns
    genre_counts = _df["genre"].value_counts()["genre"]
    all_genres = list(mappings.ROLE_GENRE_MAP.keys()) + [OTHER_GENRE_NAME]
    assert all([genre in all_genres for genre in genre_counts.unique()])
    # todo more tests


def __test_apply_pub_platform(dataframe: pl.DataFrame): ...  # noqa todo


def test_apply_main_genre(dataframe: pl.DataFrame):
    def check_all_mapped(name: str, main_genre: str) -> bool:
        return all([g == main_genre for g in _df.filter(pl.col("name") == name)["main_genre"]])

    _df = preprocess.apply_genre_affiliation(preprocess.fix_date_col(dataframe))
    _df = preprocess.apply_main_genre(_df)

    assert check_all_mapped("Ursula Weidenfeld", "Journalismus")
    assert check_all_mapped("Olivia Kortas", "Journalismus")
