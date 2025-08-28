import datetime
import json
import re
from pathlib import Path

import frontmatter
import polars as pl
from mrkdwn_analysis import MarkdownAnalyzer

from misc import Entry, Episode, Guest, Talkshow, VaultConfig


def date_loader(s: str or object) -> datetime.date:
    d = None
    formats = ["%d.%m.%Y", "%d. %B %Y"]
    for f in formats:
        try:
            d = datetime.datetime.strptime(s, f).date()
        except ValueError:
            ...
    if not d:
        raise ValueError(f"No datetime format found for s: {s}")
    return d


def drop_invalid_frontmatter_chars(data: list[str]) -> list[str]:
    # This function removes all invalid ':' characters
    for i, string in enumerate(data):
        string_parts = string.split(":")
        data[i] = f"{string_parts[0]}: {string_parts[1]}" + " ".join(string_parts[2:])
    return data


def parse_zdf_length_data(data: str) -> int:
    length_pattern = re.compile(r"PT(\d*)H(\d*)M(\d*)")
    alt_length_pattern = re.compile(r"PT(\d*)M(\d*)")
    grps = re.match(length_pattern, data)
    if grps is None:
        grps = re.match(alt_length_pattern, data).groups()
        length = int(grps[0])
    else:
        grps = grps.groups()
        length = int(grps[0]) * 60 + int(grps[1]) * 1
    return length


def load_markuslanz_addins(fp: Path) -> Episode:
    analyzer = MarkdownAnalyzer(fp)
    metainfos = frontmatter.load(str(fp)).metadata
    basic_info = json.loads(analyzer.identify_code_blocks()["Code block"][0]["content"])
    # Input looks like this: 2025-06-11T21:15:00.000000+00:00
    basic_info["episode_date"] = datetime.datetime.fromisoformat(
        basic_info["episode_date"]
    ).date()
    basic_info["length"] = parse_zdf_length_data(basic_info["length"])
    guest_data = json.loads(analyzer.identify_code_blocks()["Code block"][1]["content"])
    guests = [
        Guest(name=d["name"], role=d["role"], message=d["description"])
        for d in guest_data
    ]
    episode = Episode(
        episode_name=basic_info["episode_name"],
        date=basic_info["episode_date"],
        description=basic_info["description"],
        talkshow="markuslanz",
        src=metainfos["source"],
        factcheck=False,
        length=basic_info["length"],
        guests=guests,
    )

    return episode


def load_maybritillner_addins(fp: Path) -> Episode:
    analyzer = MarkdownAnalyzer(fp)
    metainfos = frontmatter.load(str(fp)).metadata
    basic_info = json.loads(analyzer.identify_code_blocks()["Code block"][0]["content"])
    # Input looks like this: 2025-06-11T21:15:00.000000+00:00
    basic_info["episode_date"] = datetime.datetime.fromisoformat(
        basic_info["episode_date"]
    ).date()
    basic_info["length"] = parse_zdf_length_data(basic_info["length"])
    guest_data = json.loads(analyzer.identify_code_blocks()["Code block"][1]["content"])
    guests = [Guest(name=d["name"], role=d["role"], message="") for d in guest_data]
    episode = Episode(
        episode_name=basic_info["episode_name"],
        date=basic_info["episode_date"],
        description=basic_info["episode_description"],
        talkshow="maybritillner",
        src=metainfos["source"],
        factcheck=False,
        length=basic_info["length"],
        guests=guests,
    )
    return episode


def load_maischberger_addins(fp: Path) -> Episode:
    analyzer = MarkdownAnalyzer(fp)
    metainfos = frontmatter.load(str(fp)).metadata
    guest_data = json.loads(analyzer.identify_code_blocks()["Code block"][0]["content"])
    guests = [Guest(name=d["name"], role=d["role"], message="") for d in guest_data]
    episode = Episode(
        episode_name=metainfos["episode_name"],  # noqa
        date=date_loader(metainfos["episode_date"]),
        description=metainfos["episode_description"],  # noqa
        talkshow="maischberger",
        src=metainfos["source"],
        factcheck=bool(metainfos["factcheck"]),  # noqa
        length=metainfos["length"],  # noqa
        guests=guests,
    )
    return episode


def load_hartaberfair_addins(fp: Path) -> Episode:
    analyzer = MarkdownAnalyzer(fp)
    metainfos = frontmatter.load(str(fp)).metadata
    guest_data = json.loads(analyzer.identify_code_blocks()["Code block"][0]["content"])
    guests = [Guest(name=d["name"], role=d["role"], message="") for d in guest_data]
    episode = Episode(
        episode_name=metainfos["episode_name"],  # noqa
        date=date_loader(metainfos["episode_date"]),
        description=metainfos["episode_description"],  # noqa
        talkshow="hartaberfair",
        src=metainfos["source"],
        factcheck=bool(metainfos["factcheck"]),  # noqa
        length=metainfos["length"],  # noqa
        guests=guests,
    )
    return episode


def load_carenmiosga_episode(fp: Path) -> Episode:
    analyzer = MarkdownAnalyzer(fp)
    metainfos = frontmatter.load(str(fp)).metadata
    guest_data = json.loads(analyzer.identify_code_blocks()["Code block"][0]["content"])
    guests = [
        Guest(name=d["name"], role=d["role"], message=d["description"])
        for d in guest_data
    ]
    episode = Episode(
        episode_name=metainfos["episode_name"],  # noqa
        date=date_loader(metainfos["episode_date"]),
        description=metainfos["episode_description"],  # noqa
        talkshow="carenmiosga",
        src=metainfos["source"],
        factcheck=bool(metainfos["factcheck"]),  # noqa
        length=metainfos["length"],  # noqa
        guests=guests,
    )
    return episode


LOADER_MAP = {
    "markuslanz": load_markuslanz_addins,
    "maybritillner": load_maybritillner_addins,
    "maischberger": load_maischberger_addins,
    "hartaberfair": load_hartaberfair_addins,
    "carenmiosga": load_carenmiosga_episode,
}


def load_vault_content(config: VaultConfig) -> pl.DataFrame:
    data_lines = []
    for talkshow, vault_path in config.model_dump().items():
        print(f"Loading '{talkshow}' from '{vault_path}'...")
        if talkshow not in LOADER_MAP.keys():
            raise ValueError(
                f"Talkshow currently not supported, choose {Talkshow.values()}"
            )
        for md_file in vault_path.glob("*.md"):
            print(f"Loading '{talkshow}' - file '{md_file}'...")
            data_lines.extend(LOADER_MAP[talkshow](fp=md_file).as_flat_dict())

    return pl.DataFrame(data=data_lines, schema=Entry.get_polars_schema())
