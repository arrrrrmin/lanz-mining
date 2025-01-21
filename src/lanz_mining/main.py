import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from uuid import uuid4

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from lanz_mining import params
import lanz_mining.miner.settings as local_settings


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from a history file (html search).")
    arg_parser.add_argument(
        "-t", "--talkshow",
        type=str,
        help="What type of website is expect.",
        choices=list(params.TALKSHOWS.keys()),
        required=True,
    )
    arg_parser.add_argument(
        "--file", type=Path, help="Html file of search results.", required=False
    )
    arg_parser.add_argument(
        "--url", type=str, help="A single url to look for new data.", required=False
    )
    arg_parser.add_argument(
        "--debug", action="store_true", help="Use any spider in debug mode", required=False
    )
    # arg_parser.add_argument("--save-to-db", action="store_true", help="Only used with --url <url>.")
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


def init_settings_and_dirs(is_history_crawl: bool, debug: bool) -> Settings:
    settings = get_project_settings()
    settings["PIPELINE_OUTPUT"] = f"{params.OUTPUT_DIR_CURRENT}/{uuid4()}.jsonl"
    if is_history_crawl:
        settings["PIPELINE_OUTPUT"] = f"{params.OUTPUT_DIR_HISTORY}/historic-items.jsonl"
    Path(settings["PIPELINE_OUTPUT"]).parent.mkdir(parents=True, exist_ok=True)
    settings = enforce_local_settings(settings)
    if debug:
        del settings["ITEM_PIPELINES"]
    return settings


def normalize_url(url: str, tld: str, slug_suffix: str) -> str:
    return url.replace(tld, "") if not url.startswith(slug_suffix) else url


def find_all_urls(html: str, talkshow: str) -> tuple[list[str], Path]:
    params.check_talkshow(talkshow)  # assert or None
    tld = params.TALKSHOWS[talkshow]["tld"]
    url_prefix = params.TALKSHOWS[talkshow]["url-prefix"]
    slug_suffix = params.TALKSHOWS[talkshow]["slug-suffix"]
    soup = BeautifulSoup(html, "html.parser")
    url_list = soup.find_all("a")
    url_list = filter(lambda url: url_prefix in url.get("href"), url_list)
    url_list = list(set(map(lambda url: url.get("href"), url_list)))
    url_list = [normalize_url(url, tld, slug_suffix) for url in url_list]
    out_path = params.url_export_path(talkshow)
    json.dump({"url_paths": url_list}, out_path.open("w", encoding="utf-8"), indent=4)
    return url_list, out_path


def main(args: Namespace) -> None:
    # Init output dir and set the output file
    settings = init_settings_and_dirs(args.file, args.debug)

    print(f"Writing to output file at '{settings['PIPELINE_OUTPUT']}'")

    if args.file:
        # Find links from history file (html search result page)
        print("Crawling data from history file")

        url_list, out_path = find_all_urls(args.file.open("r").read(), args.talkshow)
        print(f"Wrote list of found files to {out_path}")

        spider_cls = params.TALKSHOWS[args.talkshow]["item-spider"]
        spider_args = {"paths": url_list, "debug": args.debug}

    elif args.url:
        # Visit target url only and look for new data
        print(f"Visiting <{args.url}> to find new data")

        tld = params.TALKSHOWS[args.talkshow]["tld"]
        slug_suffix = params.TALKSHOWS[args.talkshow]["slug-suffix"]
        url = normalize_url(args.url, tld, slug_suffix)

        spider_cls = params.TALKSHOWS[args.talkshow]["item-spider"]
        spider_args = {"paths": [url], "debug": args.debug}

    else:
        # Visit the main site and check for new urls
        print("Searching for new urls on the main page")
        spider_cls = params.TALKSHOWS[args.talkshow]["list-spider"]
        spider_args = {"debug": args.debug}

    process = CrawlerProcess(settings)
    process.crawl(spider_cls, **spider_args)
    process.start()


if __name__ == "__main__":
    arguments = call_for_args()
    main(arguments)
