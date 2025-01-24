from scrapy.http import TextResponse

from lanz_mining.miner.parse import parse_lanz_episode


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
