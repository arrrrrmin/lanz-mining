from typing import Literal


class Party:
    FDP = "FDP"
    B90G = "B90G"
    LINKE = "LINKE"
    SPD = "SPD"
    CDU = "CDU"
    CSU = "CSU"
    NP = "Parteilos"
    FW = "Freie Wähler"
    BSW = "BSW"
    AFD = "AfD"


GroupEntry = Literal[
    "Aktivismus",
    "Geschichte",
    "Soziales",
    "Bildung",
    "Gesundheit",
    "Inneres",
    "Militär",
    "Rechtliches",
    "Wissenschaft",
    "Literatur",
    "Kultur",
    "Internationales",
    "Ökonomie",
    "Journalismus",
    "Politik",
    "Sonstiges",
]
