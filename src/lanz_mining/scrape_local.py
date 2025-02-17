import datetime
import time
from argparse import Namespace, ArgumentParser
from dataclasses import dataclass
from urllib.parse import urljoin

import polars as pl
from pathlib import Path
from urllib.request import Request

from scrapy.http import TextResponse

from lanz_mining.dataproc import text
from lanz_mining.dataproc.processors import CSVProcessor, norm_names
from lanz_mining.dataproc.register import TalkshowRegister
from lanz_mining.miner.items import Episode
from lanz_mining.miner.spiders.raw_spider import SPIDER_PARAMS


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Scrape information from local html files.")
    arg_parser.add_argument(
        "--input-dir",
        type=Path,
        help="Path to html files",
        required=True,
        default=Path("outputs/html/"),
    )
    arg_parser.add_argument(
        "--output-file", type=Path, help="Where to write the output csv?", required=True
    )
    arg_parser.add_argument(
        "--register",
        type=Path,
        help="Load a register from this file, pass new file to create fresh register",
        required=True,
    )

    args = arg_parser.parse_args()
    return args


@dataclass
class HtmlFile:
    """Object to hold data and information regarding a single html file"""

    talkshow: str
    url: str
    episode_name: str
    content: str
    date: datetime.date

    def __repr__(self) -> str:
        return (
            f"{self.talkshow} - {self.url} ({self.date})\n{self.episode_name}, {len(self.content)}"
        )

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
        """Loads a HtmlFile object from a filepath."""
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
            if len(episode_files) == 0:
                continue
            episode_files = sorted(episode_files, key=lambda html_file: html_file.date)
            if latest_only:
                episode_files = [episode_files[0]]
            episode_items = [html_file.to_item().as_flat_dict() for html_file in episode_files]
            result_list.extend(*episode_items)

    schema = Episode.get_polars_schema()
    return pl.DataFrame(data=result_list, orient="col", schema=schema, strict=False)


def main(args: Namespace):
    # Measure time required for computation
    load_start = time.time()
    # Debugging: load_single_html(Path("outputs/html/<talkshow>/<episode>/<file>.html"))
    dataframe = load_htmls(args.input_dir, True)
    dataframe = norm_names(dataframe)
    load_time = round(time.time() - load_start, 2)

    update_start = time.time()
    # Update or create `register` to index row-wise zsi-results
    # Create index is build from `episode_name` and `date`
    if Path(args.register).exists():
        register = TalkshowRegister.load(args.register)
        register.update(dataframe)
        register.save(args.register)
    else:
        register = TalkshowRegister(text.TOPICS)
        register.create(dataframe)
        register.save(args.register)

    update_time = round(time.time() - update_start, 2)
    process = time.time()

    # Post processing
    csv_processor = CSVProcessor(dataframe, register)
    csv_processor.dataframe.write_csv(arguments.output_file)
    print(csv_processor.dataframe.shape)
    with pl.Config(tbl_rows=-1, fmt_str_lengths=100):
        df = csv_processor.dataframe.filter(pl.col("name").str.contains("Brantner"))
        dataframe_sonstiges = csv_processor.dataframe.filter(pl.col("group").eq("Sonstiges"))
        print(dataframe_sonstiges["name", "role", "group", "party", "media"])
        print(df["name", "role", "group", "party", "media"])

    process_time = round(time.time() - process, 2)
    print(f"Load time: {load_time}")
    print(f"Update time: {update_time}")
    print(f"Process time: {process_time}")
    print("----------------------")
    print(f"Total run time: {load_time + update_time + process_time}")


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
