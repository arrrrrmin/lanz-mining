""" Compute the contexts of every row and write registers per talkshow. """

from argparse import Namespace, ArgumentParser
from pathlib import Path

import polars as pl

from lanz_mining import params
from lanz_mining.dataproc import text
from lanz_mining.dataproc.register import TalkshowRegister


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("CLI to compute contexts per guest and talkshow.")
    arg_parser.add_argument(
        "-t", "--talkshow", type=str, choices=list(params.TALKSHOWS.keys()), required=True
    )
    arg_parser.add_argument("--data", type=Path, help="Database export file (csv).", required=True)
    arg_parser.add_argument(
        "--register",
        type=Path,
        help="Load a register from this file, pass new file to create fresh register",
        required=True,
    )
    arg_parser.add_argument("--batch-size", type=int, default=16, required=False)
    args = arg_parser.parse_args()
    return args


def add_index(dataframe: pl.DataFrame) -> pl.DataFrame:
    size = dataframe.shape[0]
    index_column = pl.Series("index", range(0, size))
    return dataframe.insert_column(0, index_column)


def main(args: Namespace):
    dataframe = pl.read_csv(args.data, separator=",")
    dataframe = add_index(dataframe)
    index_cols = params.TALKSHOWS[args.talkshow]["register"]["index_cols"]
    sequence_cols = params.TALKSHOWS[args.talkshow]["register"]["sequence_cols"]

    if Path(args.register).exists():
        register = TalkshowRegister.load(args.register)
        register.update(dataframe, args.batch_size)
        register.save(args.register)
    else:
        hypothesis = params.TALKSHOWS[args.talkshow]["register"]["hypothesis"]
        register = TalkshowRegister(
            args.talkshow,
            text.TOPICS,
            hypothesis,
            index_cols,
            sequence_cols,
        )
        register.create(dataframe, args.batch_size)
        register.save(args.register)


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
