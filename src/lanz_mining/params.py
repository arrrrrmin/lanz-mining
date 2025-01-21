from pathlib import Path

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


def check_talkshow(option: str) -> None or AssertionError:
    assert option in TALKSHOWS.keys(), f"Invalid talkshow option use: {list(TALKSHOWS.keys())}"


def url_export_path(talkshow: str) -> Path:
    return Path(f"{OUTPUT_DIR_HISTORY}/{talkshow}-{URL_EXPORT_NAME}")
