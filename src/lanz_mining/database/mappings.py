# Party membership mapping aims to resolve the fuzzy role "politician".
# Other maps aim to find a more general role like "agrar" or "industry"
from datetime import date

today = date.today().strftime("%Y-%m-%d")
party_membership_map = {
    "Alexander Graf Lambsdorff": "FDP",
    "Aminata Touré": "B90G",
    "Andreas Bovenschulte": "SPD",
    "Anton Hofreiter": "B90G",
    "Belit Onay": "B90G",
    "Bernd Riexinger": "LINKE",
    "Bettina Stark-Watzinger": "FDP",
    "Boris Pistorius": "SPD",
    "Carsten Linnemann": "CDU",
    "Cem Özdemir": "B90G",
    "Christian Dürr": "FDP",
    "Christoph Ploß": "CDU",
    "Claus Ruhe Madsen": "No party",
    "Daniel Günther": "CDU",
    "Diana Kinnert": "CDU",
    "Dietmar Bartsch": "LINKE",
    "Franziska Giffey": "SPD",
    "Gerhart Baum": "FDP",
    "Gregor Gysi": "LINKE",
    "Hubert Aiwanger": "FW",
    "Hubertus Heil": "SPD",
    "Jan van Aken": "LINKE",
    "Janine Wissler": "LINKE",
    "Jens Spahn": "CDU",
    "Joe Chialo": "CDU",
    "Johannes Vogel": "FDP",
    "Johannes Winkel": "CDU",
    "Jürgen Trittin": "B90G",
    "Kai Wegner": "CDU",
    "Karin Prien": "CDU",
    "Karl Lauterbach": "SPD",
    "Katja Kipping": "LINKE",
    "Kevin Kühnert": "SPD",
    "Klara Geywitz": "SPD",
    "Klaus von Dohnanyi": "SPD",
    "Konstantin Kuhle": "FDP",
    "Lars Klingbeil": "SPD",
    "Linda Teuteberg": "FDP",
    "M.- A. Strack-Zimmermann": "FDP",
    "Manfred Weber": "CSU",
    "Marco Buschmann": "FDP",
    "Markus Söder": "CSU",
    "Martin Huber": "CSU",
    "Michael Roth": "SPD",
    "Michael Theurer": "FDP",
    "Nancy Faeser": "SPD",
    "Norbert Röttgen": "CDU",
    "Omid Nouripour": "B90G",
    "Paul Ziemiak": "CDU",
    "Peter Altmaier": "CDU",
    "Ralf Stegner": "SPD",
    "Reiner Haseloff": "CDU",
    "Ricarda Lang": "B90G",
    "Robert Habeck": "B90G",
    "Robert Lambrou": "AFD",
    "Roderich Kiesewetter": "CDU",
    "Rüdiger Lucassen": "AFD",
    "Saskia Esken": "SPD",
    "Sebastian Fiedler": "SPD",
    "Serap Güler": "CDU",
    "Sigmar Gabriel": "SPD",
    "Steffen Kotré": "AFD",
    "Steffi Lemke": "B90G",
    "Stephan Weil": "SPD",
    "Svenja Schulze": "SPD",
    "Theo Waigel": "CSU",
    "Thomas Heilmann": "CDU",
    "Thomas de Maizière": "CDU",
    "Thorsten Frei": "CDU",
    "Tino Chrupalla": "AFD",
    "Werner Henning": "CDU",
    "Winfried Kretschmann": "B90G",
    "Wolfgang Kubicki": "FDP",
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
    "politik",
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
        ]
    ),
    "Inneres": lambda role: any(
        _ in role.lower() for _ in ["sicherheitsexpert", "polizei", "polizist", "kriminal"]
    ),
}


def get_complicated_party_memberships():
    """Special cases of politicians switching their party membership at some point in time."""
    return {
        "Boris Palmer": [("1972-1-1", "2023-5-1", "B90G"), ("2023-1-5", today, "No party")],
        "Claus Ruhe Madsen": [("1972-1-1", "2023-5-1", "No party"), ("2023-5-1", today, "CDU")],
        "Jörg Meuthen": [("2015-7-1", "2022-1-28", "AFD"), ("2022-1-28", today, "No party")],
        "Sahra Wagenknecht": [("1969-7-1", "2024-1-8", "LINKE"), ("2024-1-8", today, "BSW")],
    }
