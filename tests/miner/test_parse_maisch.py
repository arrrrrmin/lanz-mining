from pathlib import Path

import pytest
from scrapy import Request
from scrapy.http import TextResponse

from lanz_mining.miner.parse import parse_maisch_episode


def test_parse_maisch_episode(maisch_example: TextResponse):
    expected_names = [
        "Robert Habeck",
        "Karl-Theodor zu Guttenberg",
        "Cherno Jobatey",
        "Helene Bubrowski",
        "Jan Fleischhauer",
    ]
    item = parse_maisch_episode(maisch_example, False).as_dict()
    assert item["name"] == "maischberger am 21.01.2025"
    assert item["date"] == "21.01.2025"
    assert item["description"].startswith(
        "Bundestagswahl 2025 – für welche Politik stehen die Grünen?"
    )
    for i, guest in enumerate(item["guests"]):
        assert "name" in guest.keys()
        assert guest["name"] in expected_names
