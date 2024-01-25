from argparse import ArgumentParser, Namespace
from pathlib import Path
from uuid import uuid4

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from lanz_mining.miner.spiders.lanz_spider import LanzSpider
from lanz_mining.params import OUTPUT_DIR_CURRENT, OUTPUT_DIR_HISTORY
from lanz_mining.utils import link_href_fn, link_filter_fn, export_url_paths
from miner.spiders.lanz_episode_spider import LanzEpisodeSpider


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from a history file (html search).")
    arg_parser.add_argument(
        "--file", type=Path, help="Html file of search results.", required=False
    )
    args = arg_parser.parse_args()
    return args


def init_output_dir(is_history_crawl: bool) -> Settings:
    settings = get_project_settings()
    settings["PIPELINE_OUTPUT"] = f"{OUTPUT_DIR_CURRENT}/{uuid4()}.jsonl"
    if is_history_crawl:
        settings["PIPELINE_OUTPUT"] = f"{OUTPUT_DIR_HISTORY}/items.jsonl"
    Path(settings["PIPELINE_OUTPUT"]).parent.mkdir(parents=True, exist_ok=True)
    return settings


def main(args):
    # Init output dir and set the output file
    settings = init_output_dir(args.file)
    print(f"Writing to output file at '{settings['PIPELINE_OUTPUT']}'")
    # Find links from history file (html search result page)
    if args.file:
        print("Crawling data from history file")

        html = args.file.open("r").read()
        soup = BeautifulSoup(html, "html.parser")
        url_list = soup.find_all("a")
        url_list = filter(link_filter_fn, url_list)
        url_list = map(link_href_fn, url_list)
        url_list = list(set(url_list))
        out_path = export_url_paths(url_list)
        print(f"Wrote list of found files to {out_path}")

        process = CrawlerProcess(settings)
        process.crawl(LanzEpisodeSpider, paths=url_list, output_path="outputs/")
        process.start()
    # Visit the main site and check for new urls
    else:
        print("Searching for new urls on the main page")

        process = CrawlerProcess(settings)
        process.crawl(LanzSpider)
        process.start()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
