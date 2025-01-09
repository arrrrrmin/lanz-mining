import json
from argparse import Namespace, ArgumentParser
from datetime import datetime
from pathlib import Path

import polars as pl

from lanz_mining.dataproc import preprocess, experts


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Process database exports from csv file and write it back as csv.")
    arg_parser.add_argument(
        "--file",
        type=Path,
        help="Html file of search results.",
        required=True,
        default=Path("exports/guests.csv"),
    )
    arg_parser.add_argument("-w", "--write", dest="write", action="store_true")
    args = arg_parser.parse_args()
    return args


def get_outfile_suffix(path: str, name: str) -> Path:
    assert Path(path).exists(), f"Base path '{path}' does not exist."
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp = Path(path) / name
    return Path(path) / f"{temp.stem}-{timestamp}{temp.suffix}"


def main(input_file: Path, write: bool):
    df = preprocess.default_preprocessing(pl.read_csv(input_file))
    df = experts.apply_expertise_column(df)

    time_range = (
        df["date"].min().strftime("%d.%m.%Y"),
        df["date"].max().strftime("%d.%m.%Y"),
    )
    num_episodes = df["lanzepisode_name"].unique().len()
    num_guests = df["name"].unique().len()
    num_genres = df["genre"].unique().len()
    num_experts = df.filter(pl.col("expertise").is_not_null())["name"].unique().count()
    genre_counts = df["genre"].value_counts().sort("count", descending=True)
    party_counts = df["party"].value_counts().drop_nulls().sort("count", descending=True)
    expert_conuts = (
        df["expertise"]
        .value_counts()
        .filter(pl.col("count") > 1)  # Filter for compact printing
        .drop_nulls()
        .sort("count", descending=True)
    )
    the_special_expert = (
        df.filter(pl.col("expertise").is_not_null()).group_by("name").agg(pl.col("expertise").unique().len()).filter(pl.col("expertise") > 1)
    )
    print(the_special_expert.sort("expertise", descending=True))
    print(df.filter(pl.col("name") == "Sascha Lobo"))

    meta = {
        "start": time_range[0],
        "end": time_range[1],
        "episodes": num_episodes,
        "guests": num_guests,
        "genres": num_genres,
        "experts": num_experts,
    }
    print(meta)
    print("All genres:", genre_counts)
    print("All political parties:", party_counts)
    print("All experts:", expert_conuts)

    if write:
        meta_out_fp = get_outfile_suffix("outputs", "meta.json")
        data_out_fp = get_outfile_suffix("outputs", "data.csv")
        json.dump(meta, meta_out_fp.open("w"), indent=4)
        df.write_csv(data_out_fp)

        print("Outputs written to:")
        print(meta_out_fp)
        print(data_out_fp)


if __name__ == "__main__":
    arguments = call_for_args()
    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        main(arguments.file, arguments.write)
