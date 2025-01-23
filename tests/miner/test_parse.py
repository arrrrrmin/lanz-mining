from scrapy.http import TextResponse

from lanz_mining.miner.items import cleanup_name
from lanz_mining.miner.parse import parse_lanz_episode, parse_illner_episode, parse_miosga_episode


def test_temp():
    import re

    lines = [
        "Bijan Djir-Sarai, FDP-Generalsekretär",
        "Annalena Baerbock (Bundesministerin des Auswärtigen, Grüne)",
        "Marie-Agnes Strack-Zimmermann, Vorsitzende des Verteidigungsausschusses des Deutschen Bundestages (FDP)"
    ]
    for l in lines:
        grps = re.search(r"\((.+)\)", l)
        print(grps is not None and len(grps.group(1)) > 5)


def test_cleanup_name():
    names = [
        "Lars Klingbeil (SPD)",
        "Alexander Dobrindt (CSU)",
        "Felix Banaszak (B´90/Die Grünen)",
        "Agnes Strack Zimmermann (FDP)",
    ]
    asserted_names = [
        "Lars Klingbeil",
        "Alexander Dobrindt",
        "Felix Banaszak",
        "Agnes Strack Zimmermann",
    ]
    _names = [cleanup_name(n) for n in names]
    for i, _n in enumerate(_names):
        assert _n == asserted_names[i]
        assert not (_n.startswith(" ") or _n.endswith(" "))


def test_parse_lanz_episode(lanz_example: TextResponse):
    item = parse_lanz_episode(lanz_example, False).as_dict()
    assert item["name"] == "Markus Lanz vom 15. Januar 2025"
    assert item["date"] == "15.01.2025"
    assert item["length"] == 75
    assert (
        item["description"]
        == "Über die Ausrichtung des Wahlkampfes der Grünen, über Russlands sogenannte Schattenflotte sowie über den Einfluss und die Gesinnung der Tech-Milliardäre Musk und Zuckerberg."
    )
    assert (
        item["guests"] is not None and isinstance(item["guests"], list) and len(item["guests"]) == 4
    )
    expected_names = ["F. Brantner", "Carlo Masala", "Robin Alexander", "Sascha Lobo"]
    expected_roles = ["Grünen-Co-Vorsitzende", "Militärexperte", "Journalist", "Journalist"]
    for i, guest in enumerate(item["guests"]):
        assert all([k in guest.keys() for k in ("name", "role", "text")])
        assert guest["name"] == expected_names[i]
        assert guest["role"] == expected_roles[i]
        assert guest["text"] is not None and len(guest["text"]) > 0


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


def test_parse_miosga_episode(miosga_example: TextResponse):
    expected_names = ["Joachim Gauck", "Julia Reuschenbach", "Steffen Mau"]
    expected_roles = ["Bundespräsident a.D.", "Politikwissenschaftlerin", "Soziologe"]
    item = parse_miosga_episode(miosga_example, False).as_dict()
    assert item["name"] == "Nach den Wahlen: Was wird aus Deutschland, Herr Gauck?"
    assert item["date"] == "22.09.2024"
    assert item["description"].startswith("Drei Wochen nach den Wahlen in Sachsen und Thüringen")
    for i, guest in enumerate(item["guests"]):
        assert all([k in guest.keys() for k in ("name", "role")])
        assert guest["name"] == expected_names[i]
        assert guest["role"] == expected_roles[i]
        assert len(guest["text"]) > 0
