from pathlib import Path
from typing import Union, Optional

import scrapy

from lanz_mining.miner.spiders.lanz_spider import LanzSpider, LanzEpisodeSpider
from lanz_mining.miner.spiders.illner_spider import IllnerSpider, IllnerEpisodeSpider


OUTPUT_DIR = "outputs"
OUTPUT_DIR_HISTORY = "outputs/history"
OUTPUT_DIR_CURRENT = "outputs/current"
URL_PREFIX_ML = "/gesellschaft/markus-lanz/markus-lanz-vom"
URL_PREFIX_MI = "/politik/maybrit-illner/"
URL_EXPORT_NAME = "found_urls.json"

TALKSHOWS = {
    "markuslanz": {
        "tld": "https://www.zdf.de",
        "url-prefix": "/gesellschaft/markus-lanz/markus-lanz-vom",
        "slug-suffix": "/gesellschaft/",
        "list-spider": LanzSpider,
        "item-spider": LanzEpisodeSpider,
    },
    "maybritillner": {
        "tld": "https://www.zdf.de",
        "url-prefix": "/politik/maybrit-illner/",
        "slug-suffix": "/politik/",
        "list-spider": IllnerSpider,
        "item-spider": IllnerEpisodeSpider,
    },
}


def detect_talkshow(url_lists: Union[list[str]]) -> Optional[str]:
    urls = [url_lists] if isinstance(url_lists, str) else url_lists
    talkshow = None
    for talkshow_key in TALKSHOWS.keys():
        for url in urls:
            if (
                TALKSHOWS[talkshow_key]["url-prefix"] in url
                and TALKSHOWS[talkshow_key]["tld"] in url
            ):
                return talkshow_key  # Early stop might be a bad idea, let's see
    return talkshow


def check_talkshow(option: str) -> None or AssertionError:
    assert option in TALKSHOWS.keys(), f"Invalid talkshow option use: {list(TALKSHOWS.keys())}"


def url_export_path(talkshow: str) -> Path:
    return Path(f"{OUTPUT_DIR_HISTORY}/{talkshow}-{URL_EXPORT_NAME}")


def spider_switch(urls: Union[str, list[str]]) -> scrapy.Spider:
    # We are either running in an --file scenario or --url (multi or single crawl)
    multi_crawl = isinstance(urls, list)
    talkshow = detect_talkshow(urls)
    spider_key = "multi-spider" if multi_crawl else "single-spider"
    return TALKSHOWS[talkshow][spider_key]
