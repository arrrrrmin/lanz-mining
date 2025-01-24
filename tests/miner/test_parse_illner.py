from scrapy.http import TextResponse

from lanz_mining.miner.parse import parse_illner_episode


def test_parse_illner_episode(illner_example: TextResponse):
    item = parse_illner_episode(illner_example, False).as_dict()
    assert item["name"] == "Viele Ideen, wenig Geld – Wahlkampf der teuren Versprechen?"
    assert item["date"] == "19.12.2024"
    assert item["length"] == 64
    expected_desciption = "In der letzten Ausgabe des Jahres diskutiert Maybrit Illner mit den Parteivorsitzenden Lars Klingbeil (SPD)"
    expected_desciption_extension = "Erst recht, wenn Deutschland wie versprochen auf Dauer das Zwei-Prozent-Ziel der Nato erfüllen will"
    assert item["description"].count(expected_desciption) == 1
    assert item["description"].count(expected_desciption_extension) == 1
    assert item["factcheck"] == False
    assert (
        item["guests"] is not None and isinstance(item["guests"], list) and len(item["guests"]) == 5
    )
    expected_names = [
        "Lars Klingbeil (SPD)",
        "Alexander Dobrindt (CSU)",
        "Felix Banaszak (B´90/Die Grünen)",
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
    for i, guest in enumerate(item["guests"]):
        assert all([k in guest.keys() for k in ("name", "role")])
        assert guest["name"] == expected_names[i]
        assert guest["role"] == expected_roles[i]
