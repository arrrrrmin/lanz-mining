from argparse import Namespace, ArgumentParser
from pathlib import Path
from typing import Any

from icecream import ic
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from lanz_mining.main import enforce_local_settings
from lanz_mining.miner.spiders.raw_spider import RecentRawSpider, SPIDER_PARAMS, SimpleRawSpider


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from files or current start page.")
    arg_parser.add_argument(
        "-t",
        "--talkshow",
        type=str,
        help="What type of website is expect.",
        choices=list(SPIDER_PARAMS.keys()),
        required=True,
    )
    arg_parser.add_argument(
        "--file", type=Path, help="Html file of search results (zdf).", required=False
    )
    args = arg_parser.parse_args()
    return args


def find_urls_from_file(file: Path, params: dict[str, Any]) -> list[str]:
    file_content = file.open("rb").read()
    init_url = params["start_url"]
    recent_episodes_fn = params["recent_episodes"]
    response = TextResponse(url=init_url, request=Request(url=init_url, body=file_content))
    episode_urls = recent_episodes_fn(response)
    episode_urls = list(
        set(filter(lambda url: all(slug in url for slug in params["allowed_slugs"]), episode_urls))
    )
    if params["excludes"]:
        episode_urls = list(
            set(filter(lambda url: all(ex not in url for ex in params["excludes"]), episode_urls))
        )
    for i, episode_url in enumerate(episode_urls):
        ic(i, episode_url)
    return episode_urls


def start_from_txt(file: Path, talkshow: str, settings: Settings) -> None:
    # Only used for maischberger
    start_urls = [line.strip() for line in file.open("r").readlines()]
    process = CrawlerProcess(settings)
    for url in start_urls:
        ic(url)
        spider_args = {"talkshow": talkshow, "start_url": url}
        spider_cls = RecentRawSpider
        process.crawl(spider_cls, **spider_args)
    process.start()


def main(args: Namespace):
    settings = enforce_local_settings(get_project_settings())
    settings.set("LOG_LEVEL", "INFO")
    if args.file:
        if args.file.suffix == ".txt":
            # Maischberger + .txt-file
            return start_from_txt(args.file, args.talkshow, settings)
        else:
            # Lanz/Illner + .txt-file
            episode_urls = find_urls_from_file(args.file, SPIDER_PARAMS[args.talkshow])
            spider_cls = SimpleRawSpider
            spider_args = {"talkshow": args.talkshow, "start_urls": episode_urls}
    else:
        # Periodic crawling for all formats
        spider_cls = RecentRawSpider
        spider_args = {"talkshow": args.talkshow}

    process = CrawlerProcess(settings)
    process.crawl(spider_cls, **spider_args)
    process.start()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
