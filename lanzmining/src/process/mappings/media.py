from process.mappings.utils import as_rpattern


MEDIA_MAPS: dict[str, str] = {
    "Süddeutsche Zeitung": as_rpattern(
        [' "sz"', "süddeutsche(.+)zeitung", " sz ", " sz-"]
    ),
    "Rheinische Post": as_rpattern(["rheinische post", "rheinischen post"]),
    "Spiegel": as_rpattern(["\(spiegel\)", '"spiegel"', "spiegel-"]),
    "FAZ": as_rpattern(
        ['"faz"', "frankfurter allgemeinen", " faz\-", " faz ", "'faz'"]
    ),
    "Bild": as_rpattern(['"bild"']),
    "TAZ": as_rpattern(['"taz"', "taz\-", "taz"]),
    "RND": as_rpattern(
        [
            '"rnd"',
            "redaktions-netzwerk deutschland",
            "redaktionsnetzwerk deutschland",
        ]
    ),
    "Zeit": as_rpattern(
        ['"zeit"', "\(zeit\)", "zeit online", "zeit\“", '"die zeit"', "'die zeit'"]
    ),
    "Tagesspiegel": as_rpattern(['"tagesspiegel"']),
    "Stern": as_rpattern(['"stern"']),
    "NZZ": as_rpattern(["neue(.+)zürcher zeitung", "nzz", "'nzz'"]),
    "Handelsblatt": as_rpattern(["handelsblatt"]),
    "The Pioneer": as_rpattern(["the pioneer", '"pioneer"', '"thepioneer"']),
    "Deutschlandradio": as_rpattern(["deutschlandradio"]),
    "Deutschlandfunk": as_rpattern(["deutschlandfunk"]),
    "Wirtschafts Woche": as_rpattern(["wirtschaftswoche", '"wirtschafts woche"']),
    "Table.Media": as_rpattern(
        ["table\.media", "table media", "table.briefings", "table briefings"]
    ),
    "ARD": as_rpattern(["ard\-", " ard", "\(ard\)"]),
    "ZDF": as_rpattern([" zdf", '"heute journal"', "\(zdf\)"]),
    "RTL": as_rpattern(['"rtl"', "rtl\-", " rtl "]),
    "FOCUS": as_rpattern(['"focus"']),
    "T-Online": as_rpattern(["t\-online"]),
    "WDR": as_rpattern(["((wdr)[\W|-].+)"]),
    "NDR": as_rpattern(["((ndr)[\W|-].+)"]),
    "CNN": as_rpattern(["((cnn)[\W|-].+)"]),
    "Wall Street Journal": as_rpattern(["wall street journal"]),
    "Washington Post": as_rpattern(["washington post"]),
    "FUNKE Mediengruppe": as_rpattern(["funke mediengruppe"]),
    "Jüdischen Allgemeinen": as_rpattern(["jüdischen allgemeinen"]),
    "Correctiv": as_rpattern(['"correctiv"']),
    "Welt": as_rpattern(['"welt"', r"\(welt\)", "welt\-"]),
    "Zenith": as_rpattern(['"zenith"']),
    "The European": as_rpattern(['"the european"']),
}
