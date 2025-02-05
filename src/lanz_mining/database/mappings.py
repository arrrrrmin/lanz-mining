# Party membership mapping aims to resolve the fuzzy role "politician".
# Other maps aim to find a more general role like "economy" or "social"
from datetime import date

from lanz_mining.database.naming import Party

TODAY = date.today().strftime("%Y-%m-%d")

# This map is used to normalise different abbreviated guest names.
# Use this map searching for the key and replace it with it's value.
MANUAL_NAME_MAP = {
    "Strack-Zimmermann": "M.-A. Strack-Zimmermann",
    "Marie-Agnes Strack-Zimmermann": "M.-A. Strack-Zimmermann",
    "Marie-A. Strack-Zimmermann": "M.-A. Strack-Zimmermann",
    "M. -A. Strack-Zimmermann": "M.-A. Strack-Zimmermann",
    "M.- A. Strack-Zimmermann": "M.-A. Strack-Zimmermann",
    "Claus R. Madsen": "Claus Ruhe Madsen",
}

# Map of names to political party membership
PARTY_MEMBERSHIP_MAP = {
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
    "M.-A. Strack-Zimmermann": Party.FDP,
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
    "Christian Engelhardt": Party.CDU,
    "Andreas Bausewein": Party.SPD,
    "Cordelia Koch": Party.B90G,
    "Sibylle Keupen": Party.NP,
    "Christian Herrgott": Party.CDU,
    "Peter Tschentscher": Party.SPD,
    "Annalena Baerbock": Party.B90G,
    "Bettina Dickes": Party.CDU,
    "Tim von Winning": Party.NP,
    "Ryyan Alshebl": Party.B90G,
    "Joachim Gauck": Party.NP,
    "Tanja Schweiger": Party.FW,
    "Jens Marco Scherf": Party.B90G,
    "Günther-Martin Pauli": Party.CDU,
    "Rita Röhrl": Party.SPD,
    "Mario Czaja": Party.CDU,
    "Wolfgang Schäuble": Party.CDU,
    "Ulrike Scharf": Party.CSU,
    "Herbert Reul": Party.CDU,
    "Jessica Rosenthal": Party.SPD,
    "Michael Kretschmer": Party.CDU,
    "Verena Hubertz": Party.SPD,
    "Frank Schäffler": Party.FDP,
    "Friedrich Merz": Party.CDU,
    "Joachim Stamp": Party.FDP,
    "Mike Mohring": Party.CDU,
    "Philipp Türmer": Party.SPD,
    "Franziska Brandmann": Party.FDP,
    "Katharina Stolla": Party.B90G,
    "René Wilke": Party.LINKE,
    "Olaf von Löwis": Party.CSU,
    "Mario Voigt": Party.CDU,
    "Philipp Amthor": Party.CDU,
    "Katrin Göring-Eckardt": Party.B90G,
    "Andy Grote": Party.SPD,
    "Svenja Appuhn": Party.B90G,
    "Franz Müntefering": Party.SPD,
    "Dagmar Schulz": Party.NP,
    "Oliver Schmidt-Gutzat": Party.SPD,
    "Wiebke Şahin-Schwarzweller": Party.FDP,
    "Bodo Ramelow": Party.LINKE,
    "Lars Bökenkröger": Party.CDU,
    "Richard Arnold": Party.CDU,
    "Felix Schwenke": Party.SPD,
    "Christine Herntier": Party.NP,
    "Yvonne Mosler": Party.B90G,
    "Fabio De Masi": Party.BSW,
    "Michael Kellner": Party.B90G,
    "Katharina Dröge": Party.B90G,
    "Andreas Audretsch": Party.B90G,
    "Marcus Faber": Party.FDP,
    "Jakob Blasel": Party.B90G,
    "Johannes Volkmann": Party.CDU,
    "Bärbel Bas": Party.SPD,
    "Peer Steinbrück": Party.SPD,
    "Klaus Müller": Party.B90G,
    "Angela Merkel": Party.CDU,
    "Felix Banaszak": Party.B90G,
    "Alexander Dobrindt": Party.CSU,
}

POLITICS_KEYWORDS = [
    "politik",
    "bürgermeister",
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
    "bundestagsabgeordnete",
    "bundestagspräsident",
    "junge liberale",
    "juso",
    "tübinger ob",
    "junge union",
    "ju-vorsitzende",
    "juso-vorsitzende",
    "jl-vorsitzende",
    "evp",
    "unionsfraktions",
    "juli-vorsitzende",
    "netzagentur" "politik-expert",
    "politikexpert",
    "fraktionsvorsitzend",
]

ROLE_GENRE_MAP = {
    "Aktivismus": lambda role: any(
        _ in role.lower() for _ in ["aktivist", "bürgerrechtler", "whistleblow", "völkerrechtler"]
    ),
    "Journalismus": lambda role: any(
        _ in role.lower() for _ in ["reporter", "journalist", "korrespondent", "redakteur"]
    ),
    "Recht": lambda role: any(
        _ in role.lower()
        for _ in ["jurist", "richter", "rechtsanwalt", "rechtsanwältin", "steuerexpert"]
    ),
    "Bildung": lambda role: any(
        _ in role.lower() for _ in ["lehrer", "pädagog", "schüler", "student", "schulleiter"]
    ),
    "Politik": lambda role: any(_ in role.lower() for _ in POLITICS_KEYWORDS),
    "Militär": lambda role: any(
        _ in role.lower() for _ in ["militär", "verteidigung", "bundeswehr", "oberst", "agent"]
    ),
    "Geschichte": lambda role: any(
        _ in role.lower() for _ in ["historiker", "zeitzeuge", "zeitzeugin", "shoah"]
    ),
    "Soziales": lambda role: any(
        _ in role.lower()
        for _ in [
            "soziolog",
            "sozialwissenschaft",
            "sozialpsycholog",
            "sozialarbeiter",
            "sprecher der arche",
            "sprecherin der arche",
        ]
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
            "nahostexpert",
            "botschafter",
            "ukraine-expert",
            "frankreich-expert",
            "osteuropa-expert",
            "türkei-expert",
            "diplomat",
            "islam-expert",
        ]
    ),
    "Wissenschaft": lambda role: any(
        _ in role.lower()
        for _ in [
            "wissenschaft",
            "forscher",
            "physiker",
            "biolog",
            "hydrologe",
            "zukunftsforscher",
            "ökolog",
            "philosoph",
            "theolog",
            "politolog",
            "politikwissenschaft",
            "islamwissenschaft",
            "extremismusforscher",
        ]
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
            "volkswirt",
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
            "suchtexpert",
            "onkologe",
        ]
    ),
    "Inneres": lambda role: any(
        _ in role.lower()
        for _ in [
            "sicherheitsexpert",
            "polizei",
            "polizist",
            "kriminal",
            "migrationsexpert",
            "integrationsexpert",
            "kriminolog",
            "migrationswissenschaft",
            "mirgationsforscher",
        ]
    ),
}

OTHER_GENRE_NAME = "Sonstiges"

ALL_GENRES = sorted(list(ROLE_GENRE_MAP.keys()), reverse=True)

PUB_PLATFORM_MAP = {
    "Welt": ['"welt"'],
    "Süddeutsche Zeitung": [' "sz"', "süddeutschen zeitung", " sz ", " sz-"],
    "Zeit": ['"zeit"', "zeit-online", "zeit online", "zeit“", '"die zeit"'],
    "Rheinische Post": ["rheinische post", "rheinischen post"],
    "Spiegel": ['"spiegel"', '"der spiegel"', "spiegel-"],
    "FAZ": ['"faz"', "frankfurter allgemeinen", " faz-", " faz "],
    "Bild": ['"bild"'],
    "TAZ": ['"taz"', "taz-"],
    "RND": [
        '"redaktionsnetzwerk deutschland"',
        '"redaktionsnetzwerks deutschland"',
        '"rnd"',
        "redaktions-netzwerk deutschland",
    ],
    "Tagesspiegel": ['"tagesspiegel"'],
    "Stern": ['"stern"'],
    "Handelsblatt": ["handelsblatt"],
    "The Pioneer": ['"the pioneer"', '"pioneer"', '"thepioneer"'],
    "Deutschlandradio": ["deutschlandradio"],
    "Deutschlandfunk": ["deutschlandfunk"],
    "Wirtschafts Woche": ["wirtschaftswoche", '"wirtschafts woche"'],
    "Table.Media": ['"table.media"', '"table media"'],
    "ZDF": ["zdf-", '"heute journal"'],
    "ARD": ["ard-"],
    "RTL": ['"rtl"', "rtl-", " rtl "],
    "FOCUS": ['"focus"'],
    "CNN": ['"cnn"', "cnn-"],
    "Correctiv": ['"correctiv"'],
    "T-Online": ["t-online"],
    "WDR": ["wdr"],
    "NDR": ["ndr"],
    "Wall Street Journal": ['"wall street journal"-'],
    "FUNKE Mediengruppe": ["funke mediengruppe"],
    "Jüdischen Allgemeinen": ['"jüdischen allgemeinen"'],
}


def get_complicated_party_memberships() -> dict[str, list[tuple[str, str, str]]]:
    """Special cases of politicians switching their party membership at some point in time."""
    return {
        "Boris Palmer": [("1972-1-1", "2023-5-1", Party.B90G), ("2023-5-1", TODAY, Party.NP)],
        "Claus R. Madsen": [("1972-1-1", "2023-5-1", Party.NP), ("2023-5-1", TODAY, Party.CDU)],
        "Jörg Meuthen": [("2015-7-1", "2022-1-28", Party.AFD), ("2022-1-28", TODAY, Party.NP)],
        "Sahra Wagenknecht": [("1969-7-1", "2024-1-8", Party.LINKE), ("2024-1-8", TODAY, "BSW")],
        "Ursula Baum": [("2004-1-1", "2014-1-1", Party.CDU), ("2014-1-1", TODAY, Party.NP)],
        "Dirk Neubauer": [("2017-1-1", "2021-1-1", Party.SPD), ("2021-1-1", TODAY, Party.NP)],
        "Katja Wolf": [("1999-1-1", "2024-1-30", Party.LINKE), ("2024-2-1", TODAY, Party.BSW)],
        "Amira Mohamed Ali": [
            ("2015-1-1", "2024-1-30", Party.LINKE),
            ("2024-2-1", TODAY, Party.BSW),
        ],
        "Melis Sekmen": [("1993-9-26", "2024-5-30", Party.B90G), ("2024-6-1", TODAY, Party.CDU)],
    }


def get_known_politicians() -> list[str]:
    """Returns all names of listed politicians"""
    list_of_politicians = list(PARTY_MEMBERSHIP_MAP.keys())
    list_of_politicians.extend(list(get_complicated_party_memberships().keys()))
    return list(set(list_of_politicians))
