from argparse import ArgumentParser, Namespace
from pathlib import Path

from lanz_mining.dataproc.datastacks import GuestGenreByYear, GuestGenreDataStack


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Process database exports from csv file.")
    arg_parser.add_argument(
        "--file",
        type=Path,
        help="Html file of search results.",
        required=True,
        default=Path("exports/guests.csv"),
    )
    args = arg_parser.parse_args()
    return args


def main(args):
    stack = GuestGenreByYear(args.file, output_file=Path("vis/guest-genre-by-year.json"))
    stack.write_data()
    stack = GuestGenreDataStack(args.file, output_file=Path("vis/guest-genre-structure.json"))
    stack.write_data()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
