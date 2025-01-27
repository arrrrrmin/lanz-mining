from scrapy.http import TextResponse

from lanz_mining.miner.parse import parse_miosga_episode


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
