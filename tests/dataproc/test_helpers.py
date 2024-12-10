from pathlib import Path
from pprint import pprint

from lanz_mining.dataproc import helpers


def test_find_unmapped_politicians_helper(file: Path) -> None:
    unknown_politicians = helpers.find_unmapped_politicians_helper(file)
    print()
    print("*** Unknown politicians ***")
    pprint(unknown_politicians)
    print()


def test_find_unmapped_roles_helper(file: Path) -> None:
    unmapped_guest_genre, no_roles = helpers.find_unmapped_roles_helper(file)
    print("*** Guests that are not yet mapped to a genre ('Other') ***:")
    pprint(sorted(unmapped_guest_genre))
    print("*** Guests without a role in raw data ***")
    pprint(no_roles)
    print()


def test_find_abbreviated_names(file: Path) -> None:
    abbreviated_names = helpers.find_abbreviated_names(file, "Zimmermann")
    print("*** All abbreviated names ***")
    pprint(abbreviated_names)
    print()


def test_find_full_date_range(file: Path) -> None:
    data_date_range = helpers.find_full_date_range(file)
    print("*** Date range ***")
    pprint(data_date_range)
    print()


def test_find_empty_message(file: Path) -> None:
    ...
