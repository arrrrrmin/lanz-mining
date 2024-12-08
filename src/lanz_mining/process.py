from argparse import ArgumentParser, Namespace
from pathlib import Path

from lanz_mining.dataproc import datastacks


DATA_DIR = Path("web/lanz-mining-page/content/docs/projects/lanzmining/data/")


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Process database exports from csv file.")
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


def main(args):
    guest_freq_stack = datastacks.GuestFrequency(
        args.file, output_file=(DATA_DIR / "guest-frequency.json")
    )
    guest_freq_dist_stack = datastacks.GuestFrequencyDist(
        args.file, output_file=(DATA_DIR / "guest-frequency-dist.json")
    )
    pol_party_dist_stack = datastacks.PoliticialPartyDist(
        args.file, output_file=(DATA_DIR / "political-party-dist.json")
    )
    guest_genre_stack = datastacks.GuestGenreDataStack(
        args.file, output_file=(DATA_DIR / "guest-genre-circle-pack.json")
    )
    stack = datastacks.GuestMessageDataStack(
        args.file, output_file=(DATA_DIR / "guest-messages.json")
    )

    if args.write:
        guest_freq_stack.write_data()
        guest_freq_dist_stack.write_data()
        pol_party_dist_stack.write_data()
        guest_genre_stack.write_data()

    # stack = datastacks.GuestGenreByYear(
    #     args.file, output_file=(DATA_DIR / "guest-genre-by-year.json")
    # )
    # stack.write_data()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
