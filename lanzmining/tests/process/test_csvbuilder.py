from pathlib import Path

import polars as pl
from _pytest.fixtures import fixture
from misc import Entry

from process import CSVBuilder


@fixture
def test_dataframe() -> pl.DataFrame:
    return pl.read_csv(
        "tests/dummy_data/test_dummy_data.csv", schema=Entry.get_polars_schema()
    )


@fixture
def test_snapshot_file() -> Path:
    return Path("tests/dummy_data/test_dummy_snapshot.csv")


def test_csvbuilder(test_dataframe: pl.DataFrame):
    builder = CSVBuilder(test_dataframe)
    assert builder.dataframe.shape == (20, 10)
    assert builder.dataframe.columns == [
        "index",
        "episode_name",
        "date",
        "description",
        "talkshow",
        "factcheck",
        "length",
        "name",
        "role",
        "message",
    ]
    builder.process()
    assert all((c in builder.dataframe.columns) for c in [])


def test_csvbuilder_merge(test_dataframe: pl.DataFrame, test_snapshot_file: Path):
    builder = CSVBuilder(test_dataframe, test_snapshot_file)
    assert builder.dataframe.shape == (25, 10)
