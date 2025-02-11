import datetime

from scrapy.http import TextResponse

from lanz_mining.miner.items import Guest
from lanz_mining.miner.parse import parse_maisch_episode


def test_parse_maisch_episode(maisch_example: TextResponse):
    expected_names = [
        "Robert Habeck",
        "Karl-Theodor zu Guttenberg",
        "Cherno Jobatey",
        "Helene Bubrowski",
        "Jan Fleischhauer",
    ]
    item = parse_maisch_episode(maisch_example, False)
    assert item.episode_name == "maischberger am 21.01.2025"
    assert item.date == datetime.datetime.strptime("21.01.2025", "%d.%m.%Y").date()
    assert item.description.startswith(
        "Bundestagswahl 2025 – für welche Politik stehen die Grünen?"
    )
    assert item.factcheck is None
    assert isinstance(item.guests, list) and len(item.guests) == 5
    assert isinstance(item.guests[0], Guest)
    for i, guest in enumerate(item.guests):
        assert guest.name in expected_names
