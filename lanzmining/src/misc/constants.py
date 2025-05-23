from typing import Any


class Type:
    @classmethod
    def values(cls) -> list[str]:
        return [v for k, v in cls.__dict__.items() if k[:1] != "_"]

    @classmethod
    def keys(cls) -> list[str]:
        return [k for k, v in cls.__dict__.items() if k[:1] != "_"]

    @classmethod
    def items(cls) -> list[tuple[Any, Any]]:
        return [(k, v) for k, v in cls.__dict__.items() if k[:1] != "_"]


class Talkshow(Type):
    MARKUSLANZ = "markuslanz"
    MAYBRITILLNER = "maybritillner"
    MAISCHBERGER = "maischberger"
    HARTABERFAIR = "hartaberfair"
    CARENMIOSGA = "carenmiosga"


class Party(Type):
    AFD = "AfD"
    B90G = "B90G"
    BSW = "BSW"
    CDU = "CDU"
    CSU = "CSU"
    FDP = "FDP"
    FW = "Freie Wähler"
    LINKE = "LINKE"
    NP = "Parteilos"
    SPD = "SPD"


class Group(Type):
    Activism = "Aktivismus"
    Culture = "Kultur"
    Domestic = "Inneres"
    Education = "Bildung"
    Economy = "Ökonomie"
    Health = "Gesundheit"
    History = "Geschichte"
    International = "Internationales"
    Journalist = "Journalismus"
    Law = "Rechtliches"
    Literatur = "Literatur"
    Military = "Militär"
    Politics = "Politik"
    Science = "Wissenschaft"
    Social = "Soziales"
    # Default
    Default = "Sonstiges"
