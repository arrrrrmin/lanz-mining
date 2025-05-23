from src.misc import Talkshow
from src.misc.constants import Party


def test_type_talkshow():
    assert all([isinstance(val, str) for val in Talkshow.values()])
    assert all([isinstance(key, str) for key in Talkshow.keys()])
    assert all([all((key, val)) for key, val in Talkshow.items()])
    assert Talkshow.values() == [
        "markuslanz",
        "maybritillner",
        "maischberger",
        "hartaberfair",
        "carenmiosga",
    ]


def test_type_party():
    assert all([isinstance(val, str) for val in Party.values()])
    assert all([isinstance(key, str) for key in Party.keys()])
    assert all([all((key, val)) for key, val in Party.items()])
    assert Party.values() == [
        "AfD",
        "B90G",
        "BSW",
        "CDU",
        "CSU",
        "FDP",
        "Freie Wähler",
        "LINKE",
        "Parteilos",
        "SPD",
    ]
