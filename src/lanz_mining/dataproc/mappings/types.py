class Type:

    @classmethod
    def properties(cls) -> list[str]:
        return [v for k, v in cls.__dict__.items() if k[:1] != '_']


class Party(Type):
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


class Group(Type):
    Activism = "Aktivismus"
    History = "Geschichte"
    Social = "Soziales"
    Education = "Bildung"
    Health = "Gesundheit"
    Domestic = "Inneres"
    Military = "Militär"
    Law = "Rechtliches"
    Science = "Wissenschaft"
    Literatur = "Literatur"
    Culture = "Kultur"
    International = "Internationales"
    Economy = "Ökonomie"
    Journalist = "Journalismus"
    Politics = "Politik"
    OptOut = "Sonstiges"


def as_rpattern(kws: list[str]) -> str:
    pattern = r"|".join(f"({kw})" for kw in kws)
    return pattern
