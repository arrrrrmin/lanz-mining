from pathlib import Path

from lanz_mining.database.naming import Party
from lanz_mining.dataproc import datastacks


def test_guest_frequency(file: Path) -> None:
    stack = datastacks.GuestFrequency(file, output_file=Path("vis/guest-genre-by-year.json"))
    # todo: find reasonable assert statements here...
    assert stack.json_data["guests"]
    assert stack.json_data["time_range"]
    assert stack.json_data["num_episodes"]
    assert stack.json_data["num_guests"]


def test_guest_genre_by_year(file: Path) -> None:
    stack = datastacks.GuestGenreByYear(file, output_file=Path("vis/guest-genre-by-year.json"))
    # todo: find reasonable assert statements here...
    assert len(stack.json_data.keys()) >= 3
    assert stack.json_data[2022]["values"]
    assert stack.json_data[2022]["genres"]
    assert stack.json_data[2022]["dates"]


def test_guest_genre_data_stack(file: Path) -> None:
    stack = datastacks.GuestGenreDataStack(file, output_file=Path("vis/guest-genre-by-year.json"))
    # todo: find reasonable assert statements here...
    assert len(stack.json_data["children"]) > 0


def test_party_dist_data_stack(file: Path) -> None:
    stack = datastacks.PoliticialPartyDist(
        file, output_file=Path("vis/political-parties-dist.json")
    )
    assert Party.FDP in stack.json_data.keys()
    assert Party.B90G in stack.json_data.keys()
    assert Party.LINKE in stack.json_data.keys()
    assert Party.SPD in stack.json_data.keys()
    assert Party.CDU in stack.json_data.keys()
    assert Party.CSU in stack.json_data.keys()
    assert Party.NP in stack.json_data.keys()
    assert Party.FW in stack.json_data.keys()
    assert Party.BSW in stack.json_data.keys()
    assert Party.AFD in stack.json_data.keys()
