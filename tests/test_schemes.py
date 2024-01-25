from datetime import datetime

from lanz_mining.params import Episode


def test_episode():
    date_str = "14.12.1999"
    length_str = "75"
    date = datetime.strptime(date_str, "%d.%m.%Y")
    ep = Episode("SomeName", date, int(length_str), "SomeDescription")
    assert ep
