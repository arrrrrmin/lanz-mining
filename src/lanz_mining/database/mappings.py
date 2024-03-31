# Party membership mapping aims to resolve the fuzzy role "politician".
# Other maps aim to find a more general role like "agrar" or "industry"
from datetime import date

from src.lanz_mining.database.naming import Party

today = date.today().strftime("%Y-%m-%d")

# This roles map is used for guests without any role in the raw data.
manual_roles_map = {
    "Rafael Laguna de la Vera": "SPRIN-D-Direktor",
    "Sabine Leutheusser-Schnarrenberger": "Ex-Bundesjustizministerin",
}

# Map of names to political party membership
party_membership_map = {
    "Alexander Graf Lambsdorff": Party.FDP,
    "Aminata Touré": Party.B90G,
    "Andreas Bovenschulte": Party.SPD,
    "Anton Hofreiter": Party.B90G,
    "Belit Onay": Party.B90G,
    "Bernd Riexinger": Party.LINKE,
    "Bettina Stark-Watzinger": Party.FDP,
    "Boris Pistorius": Party.SPD,
    "Carsten Linnemann": Party.CDU,
    "Cem Özdemir": Party.B90G,
    "Christian Dürr": Party.FDP,
    "Christoph Ploß": Party.CDU,
    "Claus Ruhe Madsen": Party.NP,
    "Daniel Günther": Party.CDU,
    "Diana Kinnert": Party.CDU,
    "Dietmar Bartsch": Party.LINKE,
    "Franziska Giffey": Party.SPD,
    "Gerhart Baum": Party.FDP,
    "Gregor Gysi": Party.LINKE,
    "Hubert Aiwanger": Party.FW,
    "Hubertus Heil": Party.SPD,
    "Jan van Aken": Party.LINKE,
    "Janine Wissler": Party.LINKE,
    "Jens Spahn": Party.CDU,
    "Joe Chialo": Party.CDU,
    "Johannes Vogel": Party.FDP,
    "Johannes Winkel": Party.CDU,
    "Jürgen Trittin": Party.B90G,
    "Kai Wegner": Party.CDU,
    "Karin Prien": Party.CDU,
    "Karl Lauterbach": Party.SPD,
    "Katja Kipping": Party.LINKE,
    "Kevin Kühnert": Party.SPD,
    "Klara Geywitz": Party.SPD,
    "Klaus von Dohnanyi": Party.SPD,
    "Konstantin Kuhle": Party.FDP,
    "Lars Klingbeil": Party.SPD,
    "Linda Teuteberg": Party.FDP,
    "M.- A. Strack-Zimmermann": Party.FDP,
    "Manfred Weber": Party.CSU,
    "Marco Buschmann": Party.FDP,
    "Markus Söder": Party.CSU,
    "Martin Huber": Party.CSU,
    "Michael Roth": Party.SPD,
    "Michael Theurer": Party.FDP,
    "Nancy Faeser": Party.SPD,
    "Norbert Röttgen": Party.CDU,
    "Omid Nouripour": Party.B90G,
    "Paul Ziemiak": Party.CDU,
    "Peter Altmaier": Party.CDU,
    "Ralf Stegner": Party.SPD,
    "Reiner Haseloff": Party.CDU,
    "Ricarda Lang": Party.B90G,
    "Robert Habeck": Party.B90G,
    "Robert Lambrou": Party.AFD,
    "Roderich Kiesewetter": Party.CDU,
    "Rüdiger Lucassen": Party.AFD,
    "Saskia Esken": Party.SPD,
    "Sebastian Fiedler": Party.SPD,
    "Sabine Leutheusser-Schnarrenberger": Party.FDP,
    "Serap Güler": Party.CDU,
    "Sigmar Gabriel": Party.SPD,
    "Steffen Kotré": Party.AFD,
    "Steffi Lemke": Party.B90G,
    "Stephan Weil": Party.SPD,
    "Svenja Schulze": Party.SPD,
    "Theo Waigel": Party.CSU,
    "Thomas Heilmann": Party.CDU,
    "Thomas de Maizière": Party.CDU,
    "Thorsten Frei": Party.CDU,
    "Tino Chrupalla": Party.AFD,
    "Werner Henning": Party.CDU,
    "Winfried Kretschmann": Party.B90G,
    "Wolfgang Kubicki": Party.FDP,
}
politics_keywords = [
    "politiker",
    "generalsekretär",
    "landrätin",
    "landrat",
    "minister",
    "kanzler",
    "linke",
    "spd",
    "grüne",
    "csu",
    "freie wähler",
    "fdp",
    "cdu",
    "bsw",
    "afd",
    "bundespräsident",
    "diplomat",
]
role_genre_map = {
    "Aktivismus": lambda role: any(
        _ in role.lower() for _ in ["aktivist", "bürgerrechtler", "whistleblow"]
    ),
    "Journalismus": lambda role: any(
        _ in role.lower() for _ in ["reporter", "journalist", "korrespondent"]
    ),
    "Recht": lambda role: any(
        _ in role.lower() for _ in ["jurist", "richter", "rechtsanwalt", "rechtsanwältin"]
    ),
    "Politik": lambda role: any(_ in role.lower() for _ in politics_keywords),
    "Bildung": lambda role: any(
        _ in role.lower() for _ in ["lehrer", "pädagog", "schüler", "student", "schulleiter"]
    ),
    "Geisteswissenschaft": lambda role: any(
        _ in role.lower()
        for _ in [
            "philosoph",
            "theolog",
            "politolog",
            "politikwissenschaft",
            "islamwissenschaft",
            "migrationswissenschaft",
            "mirgationsforscher",
            "extremismusforscher",
        ]
    ),
    "Ethik": lambda role: any(_ in role.lower() for _ in ["ethik"]),
    "Militär": lambda role: any(
        _ in role.lower() for _ in ["militär", "verteidigung", "bundeswehr"]
    ),
    "Geschichte": lambda role: any(
        _ in role.lower() for _ in ["historiker", "zeitzeuge", "zeitzeugin", "shoah"]
    ),
    "Soziales": lambda role: any(
        _ in role.lower()
        for _ in ["soziolog", "sozialwissenschaft", "sozialpsycholog", "sozialarbeiter"]
    ),
    "Naturwissenschaft": lambda role: any(
        _ in role.lower() for _ in ["wissenschaft", "forscher", "physiker", "biolog"]
    ),
    "Literatur": lambda role: any(
        _ in role.lower() for _ in ["autor", "schriftsteller", "publizist"]
    ),
    "Agrar": lambda role: any(_ in role.lower() for _ in ["agrar", "landwirt", "förster"]),
    "Ökonomie": lambda role: any(
        _ in role.lower()
        for _ in [
            "wirtschaft",
            "ökonom",
            "vorstand",
            "vw-chef",
            "manager",
            "industrie",
            "unternehmer",
            "unternehmensberater",
        ]
    ),
    "Gesundheit": lambda role: any(
        _ in role.lower()
        for _ in [
            "arzt",
            "ärztin",
            "pharmazeut",
            "psychiater",
            "mediziner",
            "virolog",
            "psycholog",
            "gynäkolog",
            "pharmakolog",
            "gesundheit",
            "radiolog",
        ]
    ),
    "Inneres": lambda role: any(
        _ in role.lower() for _ in ["sicherheitsexpert", "polizei", "polizist", "kriminal"]
    ),
    "International": lambda role: any(
        _ in role.lower()
        for _ in [
            "afrika-expert",
            "asien-expert",
            "china-expert",
            "russland-expert",
            "iran-expert",
            "amerika-expert",
            "usa-expert",
            "nahost-expert",
            "botschafter",
            "ukraine-expert",
            "frankreich-expert",
            "osteuropa-expert",
            "türkei-expert",
        ]
    ),
}


def get_complicated_party_memberships():
    """Special cases of politicians switching their party membership at some point in time."""
    return {
        "Boris Palmer": [("1972-1-1", "2023-5-1", Party.B90G), ("2023-1-5", today, Party.NP)],
        "Claus Ruhe Madsen": [("1972-1-1", "2023-5-1", Party.NP), ("2023-5-1", today, Party.CDU)],
        "Jörg Meuthen": [("2015-7-1", "2022-1-28", Party.AFD), ("2022-1-28", today, Party.NP)],
        "Sahra Wagenknecht": [("1969-7-1", "2024-1-8", Party.LINKE), ("2024-1-8", today, "BSW")],
    }


def get_known_politicians() -> list[str]:
    list_of_politicians = list(party_membership_map.keys())
    list_of_politicians.extend(list(get_complicated_party_memberships().keys()))
    return list(set(list_of_politicians))
