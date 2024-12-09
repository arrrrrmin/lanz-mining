import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from uuid import uuid4

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from lanz_mining import params
from lanz_mining.miner.spiders.lanz_debug_spider import LanzDebugSpider
from lanz_mining.miner.spiders.lanz_spider import LanzSpider
from miner.spiders.lanz_episode_spider import LanzEpisodeSpider
import miner.settings as local_settings


link_filter_fn = lambda url: params.URL_PREFIX in url.get("href")
link_href_fn = lambda url: url.get("href")


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from a history file (html search).")
    arg_parser.add_argument(
        "--file", type=Path, help="Html file of search results.", required=False
    )
    arg_parser.add_argument(
        "--url", type=str, help="A single url to look for new data.", required=False
    )
    args = arg_parser.parse_args()
    return args


def enforce_local_settings(settings: Settings) -> Settings:
    settings["LOG_LEVEL"] = local_settings.LOG_LEVEL
    settings["ROBOTSTXT_OBEY"] = local_settings.ROBOTSTXT_OBEY
    settings["DOWNLOAD_DELAY"] = local_settings.DOWNLOAD_DELAY
    settings["COOKIES_ENABLED"] = local_settings.COOKIES_ENABLED
    settings["ITEM_PIPELINES"] = local_settings.ITEM_PIPELINES
    settings["AUTOTHROTTLE_ENABLED"] = local_settings.AUTOTHROTTLE_ENABLED
    settings["AUTOTHROTTLE_START_DELAY"] = local_settings.AUTOTHROTTLE_START_DELAY
    settings["AUTOTHROTTLE_MAX_DELAY"] = local_settings.AUTOTHROTTLE_MAX_DELAY
    settings["AUTOTHROTTLE_TARGET_CONCURRENCY"] = local_settings.AUTOTHROTTLE_TARGET_CONCURRENCY
    settings["TWISTED_REACTOR"] = local_settings.TWISTED_REACTOR
    return settings


def export_url_paths(url_paths: list[str], export_path: str = params.URL_EXPORT_PATH) -> Path:
    out_path = Path(export_path)
    json.dump({"url_paths": url_paths}, out_path.open("w", encoding="utf-8"), indent=4)
    return out_path


def init_output_dir(is_history_crawl: bool) -> Settings:
    settings = get_project_settings()
    settings["PIPELINE_OUTPUT"] = f"{params.OUTPUT_DIR_CURRENT}/{uuid4()}.jsonl"
    if is_history_crawl:
        settings["PIPELINE_OUTPUT"] = f"{params.OUTPUT_DIR_HISTORY}/historic-items.jsonl"
    Path(settings["PIPELINE_OUTPUT"]).parent.mkdir(parents=True, exist_ok=True)
    return enforce_local_settings(settings)


def normalize_urls(urls: list[str]) -> list[str]:
    return [
        url.replace("https://www.zdf.de", "") if not url.startswith("/gesellschaft/") else url
        for url in urls
    ]


def main(args):
    # Init output dir and set the output file
    settings = init_output_dir(args.file)
    print(f"Writing to output file at '{settings['PIPELINE_OUTPUT']}'")

    if args.file:  # Find links from history file (html search result page)
        print("Crawling data from history file")

        html = args.file.open("r").read()
        soup = BeautifulSoup(html, "html.parser")
        url_list = soup.find_all("a")
        url_list = filter(link_filter_fn, url_list)
        url_list = map(link_href_fn, url_list)
        url_list = list(set(url_list))
        url_list = normalize_urls(url_list)
        out_path = export_url_paths(url_list)
        print(f"Wrote list of found files to {out_path}")

        process = CrawlerProcess(settings)
        process.crawl(LanzEpisodeSpider, paths=url_list, output_path="outputs/")
        process.start()

    elif args.url:  # Visit target url only and look for new data
        print(f"Visiting <{args.url}> to find new data")
        process = CrawlerProcess(settings)
        process.crawl(LanzDebugSpider, target_url=args.url)
        process.start()

    else:  # Visit the main site and check for new urls
        print("Searching for new urls on the main page")

        process = CrawlerProcess(settings)
        process.crawl(LanzSpider)
        process.start()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
