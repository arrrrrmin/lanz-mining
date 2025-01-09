import polars as pl
from _pytest.fixtures import fixture


@fixture
def dataframe() -> pl.DataFrame:
    return pl.read_csv("tests/data/guests.csv", separator=",")
