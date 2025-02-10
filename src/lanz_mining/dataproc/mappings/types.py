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


def as_rpattern(kws: list[str]) -> str:
    pattern = r"|".join(f"({kw})" for kw in kws)
    return pattern
