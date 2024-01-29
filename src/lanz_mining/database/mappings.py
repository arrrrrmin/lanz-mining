# Party membership mapping aims to resolve the fuzzy role "politician".

import datetime

today = datetime.date.today().strftime("%Y-%m-%d")
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


def create_complicated_party_memberships():
    return {
        "Boris Palmer": [("1972-1-1", "2023-5-1", "B90G"), ("2023-1-5", today, "No party")],
        "Claus Ruhe Madsen": [("1972-1-1", "2023-5-1", "No party"), ("2023-5-1", today, "CDU")],
        "Jörg Meuthen": [("2015-7-1", "2022-1-28", "AFD"), ("2022-1-28", today, "No party")],
        "Sahra Wagenknecht": [("1969-7-1", "2024-1-8", "LINKE"), ("2024-1-8", today, "BSW")],
    }


def find_party_membership(name: str, date: str) -> str or None:
    membership = None
    if name in party_membership_map.keys():
        membership = party_membership_map[name]
    elif name in party_membership_map.keys():
        compilcated_membership_map = create_complicated_party_memberships()
        if name in compilcated_membership_map.keys():
            membership_ranges = compilcated_membership_map[name]
            for start, end, party in membership_ranges:
                start = datetime.datetime.strptime(start, "%Y-%m-%d")
                end = datetime.datetime.strptime(end, "%Y-%m-%d")
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
                if start <= date < end:
                    membership = party
                    break

    return membership
