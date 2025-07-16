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
    History = "Geschichte"
    Social = "Soziales"
    Education = "Bildung"
    Health = "Gesundheit"
    Domestic = "Inneres"
    Military = "Militär"
    Law = "Recht"
    Science = "Naturwissenschaft"
    Humanities = "Geisteswissenschaft"
    Literatur = "Literatur"
    Culture = "Kultur"
    International = "Internationales"
    Economy = "Wirtschaft"
    Journalist = "Journalismus"
    Politics = "Politik"
    Sports = "Sport"
    Default = "Sonstige"
