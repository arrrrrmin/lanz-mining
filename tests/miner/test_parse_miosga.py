import datetime

from scrapy.http import TextResponse

from lanz_mining.miner.items import Guest
from lanz_mining.miner.parse import parse_miosga_episode


def test_parse_miosga_episode(miosga_example: TextResponse):
    expected_names = ["Joachim Gauck", "Julia Reuschenbach", "Steffen Mau"]
    expected_roles = ["Bundespräsident a.D.", "Politikwissenschaftlerin", "Soziologe"]
    item = parse_miosga_episode(miosga_example, False)
    assert item.episode_name == "Nach den Wahlen: Was wird aus Deutschland, Herr Gauck?"
    assert item.date == datetime.datetime.strptime("22.09.2024", "%d.%m.%Y").date()
    assert item.description.startswith("Drei Wochen nach den Wahlen in Sachsen und Thüringen")
    assert item.factcheck == False
    assert isinstance(item.guests, list) and len(item.guests) == 3
    assert isinstance(item.guests[0], Guest)
    for i, guest in enumerate(item.guests):
        assert guest.name == expected_names[i]
        assert guest.role == expected_roles[i]
        assert len(guest.message) > 0
