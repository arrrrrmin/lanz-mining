import datetime

from scrapy.http import TextResponse

from lanz_mining.miner.items import Guest
from lanz_mining.miner.parse import parse_illner_episode


def test_parse_illner_episode(illner_example: TextResponse):
    item = parse_illner_episode(illner_example, False)
    assert item.episode_name == "Viele Ideen, wenig Geld – Wahlkampf der teuren Versprechen?"
    assert item.date == datetime.datetime.strptime("19.12.2024", "%d.%m.%Y").date()
    assert item.length == 64
    expected_desciption = "In der letzten Ausgabe des Jahres diskutiert Maybrit Illner mit den Parteivorsitzenden Lars Klingbeil (SPD)"
    expected_desciption_extension = "Erst recht, wenn Deutschland wie versprochen auf Dauer das Zwei-Prozent-Ziel der Nato erfüllen will"
    assert item.description.count(expected_desciption) == 1
    assert item.description.count(expected_desciption_extension) == 1
    assert item.factcheck == False
    assert isinstance(item.guests, list) and len(item.guests) == 5
    assert isinstance(item.guests[0], Guest)
    assert [g is not None for g in item.guests]
    expected_names = [
        "Lars Klingbeil",
        "Alexander Dobrindt",
        "Felix Banaszak",
        "Juli Zeh",
        "Helene Bubrowski",
    ]
    expected_roles = [
        "Parteivorsitzender",
        "Unionsfraktionsvize, CSU-Landesgruppenchef",
        "Parteivorsitzender",
        "Schriftstellerin, Juristin, Richterin am Verfassungsgericht Land Brandenburg",
        "stellvertretende Chefredakteurin von „Table Media“",
    ]
    for i, guest in enumerate(item.guests):
        assert guest.name == expected_names[i]
        assert guest.role == expected_roles[i]
