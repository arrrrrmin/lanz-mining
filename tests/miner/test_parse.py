from datetime import datetime

from lanz_mining.miner.items import cleanup_name
from lanz_mining.miner.parse import match_datestr


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


def test_match_datestr():
    date_strings = ["24.11.2020", "05.04.2023", "18.03.20"]
    assert match_datestr(date_strings[0], 4, True)
    assert match_datestr(date_strings[0], 4, True)
    assert match_datestr(date_strings[0], 2, True)


def test_match_datestr_fallback():
    date_strings = ["18.03.20", "04.03.2020"]
    today = datetime.today().strftime("%d.%m.%Y")
    assert match_datestr(date_strings[0], 4, False) == today
    assert match_datestr(date_strings[1], 4, False) == "04.03.2020"
    assert match_datestr("String with no date", 4, True) is None
    assert match_datestr("String with no date", 2, True) is None
