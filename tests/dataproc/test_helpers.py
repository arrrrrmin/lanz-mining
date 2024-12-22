import datetime
import polars as pl

from pathlib import Path
from _pytest.fixtures import fixture

from lanz_mining.dataproc import preprocess


@fixture
def dataframe(file: Path) -> pl.DataFrame:
    return preprocess.default_preprocessing(pl.read_csv(file.open("r")))


def find_full_date_range(input_file: Path) -> dict[str, datetime.datetime]:
    df = pl.read_csv(input_file.open("r"))
    df = preprocess.default_preprocessing(df)
    return {"start": df["date"].min(), "end": df["date"].max()}


def test_find_unmapped_politicians_helper(dataframe: pl.DataFrame) -> None:
    unknown_pol = dataframe.filter(pl.col("genre") == "Politik").filter(pl.col("party").is_null())
    print()
    print("*** Unknown politicians ***")
    print(unknown_pol)
    print()


def test_find_unmapped_roles_helper(dataframe: pl.DataFrame) -> None:
    unmapped_guest_genre = dataframe.filter(pl.col("genre") == "Other")["role"]
    no_roles = dataframe.filter(pl.col("role").is_null())
    print("*** Guests that are not yet mapped to a genre ('Other') ***:")
    print(sorted(unmapped_guest_genre))
    print("*** Guests without a role in raw data ***")
    print(no_roles)
    print()


def test_find_abbreviated_names(dataframe: pl.DataFrame) -> None:
    abbreviated_names = (
        dataframe.filter(pl.col("name").str.contains_any([".", "-"]))["name"].unique().to_list()
    )
    print("*** All abbreviated names ***")
    print(abbreviated_names)
    print()


def test_find_full_date_range(dataframe: pl.DataFrame) -> None:
    print("*** Date range ***")
    print({"start": dataframe["date"].min(), "end": dataframe["date"].max()})
    print()


def test_find_empty_message(dataframe: pl.DataFrame) -> None:
    empty_messages = dataframe.filter(pl.col("message").str.len_chars() == 0)
    print("*** Empty messages ***")
    print(empty_messages)


def test_find_unmapped_newspapers(dataframe: pl.DataFrame) -> None:
    no_newspaper = dataframe.filter(pl.col("genre") == "Journalismus").filter(
        pl.col("pub_platform").is_null()
    )
    print("*** Journalists with unmapped newspaper ***")
    print(no_newspaper)
    print("*** Corresponding messages ***")
    for m in no_newspaper["name", "role", "genre", "message"].to_numpy():
        print(m)
