from pathlib import Path

from lanz_mining.dataproc.processors import (
    LanzProcessor,
    IllnerProcessor,
    MiosgaProcessor,
    MaischProcessor,
)
from lanz_mining.miner.spiders.lanz_spider import LanzSpider, LanzEpisodeSpider
from lanz_mining.miner.spiders.illner_spider import IllnerSpider, IllnerEpisodeSpider
from lanz_mining.miner.spiders.maisch_spider import MaischSpider, MaischEpisodeSpider
from lanz_mining.miner.spiders.miosga_spider import MiosgaSpider, MiosgaEpisodeSpider

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
        # No excludes needed
        "file": {"spider": LanzEpisodeSpider, "args": {}},
        "url": {"spider": LanzEpisodeSpider, "args": {}},
        "default": {"spider": LanzSpider, "args": {}},
        "processor": LanzProcessor,
        "register": {
            "index_cols": ["lanzepisode_name", "name"],
            "sequence_cols": ["message", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "maybritillner": {
        "tld": "https://www.zdf.de",
        "url-prefix": "/politik/maybrit-illner/",
        "slug-suffix": "/politik/",
        # No excludes needed
        "file": {"spider": IllnerEpisodeSpider, "args": {}},
        "url": {"spider": IllnerEpisodeSpider, "args": {}},
        "default": {"spider": IllnerSpider, "args": {}},
        "processor": IllnerProcessor,
        "register": {
            "index_cols": ["illnerepisode_name", "name"],
            "sequence_cols": ["description", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "carenmiosga": {
        "tld": "https://www.daserste.de",
        "url-prefix": "/information/talk/caren-miosga/sendung/",
        "slug-suffix": "/caren-miosga/sendung/",
        "excludes": ["/videos/web-only", "index.html"],
        "file": {"spider": MiosgaSpider, "args": {"crawl_first": False}},
        "url": {"spider": MiosgaEpisodeSpider, "args": {}},
        "default": {"spider": MiosgaSpider, "args": {"crawl_first": True}},
        "processor": MiosgaProcessor,
        "register": {
            "index_cols": ["miosgaepisode_name", "name"],
            "sequence_cols": ["message", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "maischberger": {
        "tld": "https://www.daserste.de",
        "url-prefix": "/information/talk/maischberger/sendung/",
        "slug-suffix": "/maischberger/sendung/",
        "excludes": ["-sendungen-filter", "index.html"],
        "file": {"spider": MaischEpisodeSpider, "args": {"crawl_first": False}},
        "url": {"spider": MaischEpisodeSpider, "args": {}},
        "default": {"spider": MaischSpider, "args": {"crawl_first": True}},
        "processor": MaischProcessor,
        "register": None,  # Currently not available
    },
}


def check_talkshow(option: str) -> None or AssertionError:
    assert option in TALKSHOWS.keys(), f"Invalid talkshow option use: {list(TALKSHOWS.keys())}"


def url_export_path(talkshow: str) -> Path:
    return Path(f"{OUTPUT_DIR_HISTORY}/{talkshow}-{URL_EXPORT_NAME}")
