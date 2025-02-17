import datetime

from scrapy.http import TextResponse

from lanz_mining.miner.items import Guest
from lanz_mining.miner.parse import parse_haf_episode


def test_parse_haf_episode(hartaberfair_example: TextResponse):
    expected_names = [
        "Ricarda Lang",
        "Dorothee Bär",
        "Romy Stangl",
        "Collien Ulmen-Fernandes",
        "Fikri Anıl Altıntaş",
        "Frauke Rostalski",
    ]
    expected_roles = [
        "bis November 2024 Parteivorsitzende, B‘90/Grüne",
        "Stellvertretende Parteivorsitzende, CSU",
        "kämpft mit dem Verein One Billion Rising für den Schutz von Frauen und erlebte selbst häusliche Gewalt",
        "Schauspielerin und Moderatorin",
        "Autor, Botschafter der UN-Kampagne #HeForShe",
        "Rechtswissenschaftlerin, Philosophin und Mitglied des Deutschen Ethikrats",
    ]
    episode = parse_haf_episode(hartaberfair_example, False)
    guests = episode.guests
    assert episode.episode_name == "Hass und Gewalt gegen Frauen: Ist Empörung genug?"
    assert episode.date == datetime.datetime(2024, 12, 2).date()
    assert (
        episode.description
        == "Gewalt und Hass gegen Frauen sind Alltag. Und die Straftaten gegen Frauen nehmen noch zu. In Deutschland wurden im vergangenen Jahr 360 Frauen getötet, weil sie Frauen waren. Was muss getan werden, um Frauen besser zu schützen? Kann das von Rot-Grün vorgelegte Gewalthilfegesetz etwas ändern? Welche Formen von Ungerechtigkeit und Benachteiligung erleben Frauen?"
    )
    assert episode.talkshow == "hartaberfair"
    assert episode.factcheck == True
    assert episode.length == 60
    assert all([isinstance(g, Guest) for g in guests])
    assert all([g.name is not None and g.role is not None for g in guests])
    for i, g in enumerate(guests):
        assert g.name == expected_names[i]
        assert g.role == expected_roles[i]
