import datetime
from dataclasses import dataclass
from urllib.parse import urljoin
from typing import Any, Optional

import polars as pl
import requests
from pathlib import Path
from urllib.request import Request

from scrapy.http import TextResponse

from lanz_mining.miner.items import Episode
from lanz_mining.miner.spiders.raw_spider import SPIDER_PARAMS


def fetch_wikidata(guest_name: str) -> Optional[dict[str, Any]]:
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": guest_name,
        "language": "de",
    }
    try:
        return requests.get(url, params=params).json()
    except BaseException as e:
        print(e)
        return None


@dataclass
class HtmlFile:
    """Object to hold data and information regarding a single html file"""

    talkshow: str
    url: str
    episode_name: str
    content: str
    date: datetime.date

    @property
    def parse_fn(self):
        return SPIDER_PARAMS[self.talkshow]["parse_fn"]

    def to_item(self) -> Episode:
        response = TextResponse(
            url=self.url, request=Request(url=self.url), body=self.content.encode("utf-8")
        )
        try:
            item = self.parse_fn(response, False)
        except BaseException as exception:
            raise exception
        return item

    @staticmethod
    def date_from_filename(string: str) -> datetime.date:
        """Assumes file names like [date]=[name].html"""
        y, m, d = string.split("=")[0].split("-")
        return datetime.date(int(y), int(m), int(d))

    @classmethod
    def from_path(cls, path: Path):
        """Loads a HtmlFile object from a filepath"""
        episode_name = path.parents[0].name
        date = cls.date_from_filename(path.name)
        talkshow = path.parents[1].name
        start_url = SPIDER_PARAMS[talkshow]["start_url"]
        url = urljoin(start_url, f"{episode_name}.html")
        content = path.open("rb").read().decode("utf-8")
        return cls(talkshow, url, episode_name, content, date)


def load_single_html(html_file: Path) -> Episode:
    episode_file = HtmlFile.from_path(html_file)
    try:
        result_item = episode_file.to_item()
    except BaseException as e:
        print(e)
        raise e
    return result_item


def load_htmls(html_dir: Path, latest_only: bool) -> pl.DataFrame:
    result_list = []
    for directory in html_dir.glob("./*/"):
        for episode in directory.glob("./*/"):
            episode_files: list[HtmlFile] = [
                HtmlFile.from_path(file) for file in episode.glob("*.html")
            ]
            episode_files = sorted(episode_files, key=lambda html_file: html_file.date)
            if latest_only:
                episode_files = [episode_files[0]]
            episode_items = [html_file.to_item().as_flat_dict() for html_file in episode_files]
            result_list.extend(*episode_items)

    schema = Episode.get_schema()
    return pl.DataFrame(data=result_list, orient="col", schema=schema, strict=False)


def main():
    html_dir = Path("outputs/html/")
    dataframe = load_htmls(html_dir, True)
    dataframe.write_csv("dataframe.csv")
    # for debugging:
    # load_single_html(Path("outputs/html/markuslanz/markus-lanz-vom-6-februar-2025-100/2025-02-06=index.html"))
    pass


if __name__ == "__main__":
    main()
