import polars as pl
from _pytest.fixtures import fixture

from lanz_mining.miner.items import Episode


@fixture
def dataframe() -> pl.DataFrame:
    return pl.read_csv(
        "tests/data/dataframe.csv", separator=",", schema=Episode.get_polars_schema()
    )
