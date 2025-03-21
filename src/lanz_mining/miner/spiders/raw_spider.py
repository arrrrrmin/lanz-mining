import datetime
import logging
from pathlib import Path
from typing import Any, Callable, Optional
from urllib.parse import urlparse

import scrapy
from scrapy.http import Response

from lanz_mining.miner import parse


def find_zdf_mediathek_episodes(response: Response) -> list[str]:
    # Latest episode for lanz and illner
    # urls = response.xpath("//article/div/div/div/div[2]/div/h3/a/@href").getall()
    urls = response.xpath('//*[@id="EPISODES"]/ol/li/div/div[2]/h3/a/@href').getall()
    return urls


def find_ard_episodes(response: Response) -> list[str]:
    return response.xpath("//a/@href").getall()


def follow_default_cb(
    response: Response, output_path: Path, log_cb: Callable, **_: dict[str, Any]
) -> None:
    file = urlparse(response.url).path.split("/")[-1]
    today = datetime.date.today().strftime("%Y-%m-%d")
    current_path = Path(output_path / file.rstrip(".html"))
    current_path.mkdir(exist_ok=True, parents=True)
    write_file = Path(current_path / f"{today}=index.html")
    write_file.write_bytes(response.body)
    log_cb(f"write_file - {write_file}", logging.INFO)
    return None


SPIDER_PARAMS = {
    "markuslanz": {
        "start_url": "https://www.zdf.de/talk/markus-lanz-114",
        "allowed_domains": ["www.zdf.de"],
        "allowed_slugs": ["/video/talk/markus-lanz-114/"],
        "excludes": ["presse-podcast-lanz-und-precht"],
        "recent_episodes": find_zdf_mediathek_episodes,
        "follow_cb": follow_default_cb,
        "parse_fn": parse.parse_lanz_episode,
        "register": {
            "index_cols": ["lanzepisode_name", "name"],
            "sequence_cols": ["message", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "maybritillner": {
        "start_url": "https://www.zdf.de/talk/maybrit-illner-128",
        "allowed_domains": ["www.zdf.de"],
        "allowed_slugs": ["/video/talk/maybrit-illner-128/"],
        "excludes": None,
        "recent_episodes": find_zdf_mediathek_episodes,
        "follow_cb": follow_default_cb,
        "parse_fn": parse.parse_illner_episode,
        "register": {
            "index_cols": ["illnerepisode_name", "name"],
            "sequence_cols": ["description", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "carenmiosga": {
        "start_url": "https://www.daserste.de/information/talk/caren-miosga/",
        "allowed_domains": ["www.daserste.de"],
        "allowed_slugs": ["/information/talk/caren-miosga/sendung/"],
        "excludes": ["/videos/web-only", "index.html"],
        "recent_episodes": find_ard_episodes,
        "follow_cb": follow_default_cb,
        "parse_fn": parse.parse_miosga_episode,
        "register": {
            "index_cols": ["miosgaepisode_name", "name"],
            "sequence_cols": ["message", "name", "role"],
            "hypothesis": "Die Person äußert sich zu {}.",
        },
    },
    "maischberger": {
        "start_url": "https://www.daserste.de/information/talk/maischberger/",
        "allowed_domains": ["www.daserste.de"],
        "allowed_slugs": ["/information/talk/maischberger/sendung/"],
        "excludes": ["-sendungen-filter", "index"],
        "recent_episodes": find_ard_episodes,
        "follow_cb": follow_default_cb,
        "parse_fn": parse.parse_maisch_episode,
    },
    "hartaberfair": {
        "start_url": "https://www1.wdr.de/daserste/hartaberfair/sendungen/",
        "allowed_domains": ["www1.wdr.de"],
        "allowed_slugs": ["daserste/hartaberfair/sendungen/"],
        "excludes": ["index"],
        "recent_episodes": find_ard_episodes,
        "follow_cb": follow_default_cb,
        "parse_fn": parse.parse_haf_episode,
    },
}
OUTPUT_DIR = Path("outputs/html")


class RecentRawSpider(scrapy.Spider):
    name: str = "simple-raw-spider"
    allowed_slugs: list[str]
    allowed_domains: list[str]

    def __init__(
        self,
        talkshow: str,
        start_url: Optional[str] = None,
        latest_only: bool = False,
        *args,
        **kwargs,
    ):
        super(RecentRawSpider, self).__init__(*args, **kwargs)
        self.talkshow = talkshow
        self.start_url = SPIDER_PARAMS[talkshow]["start_url"]
        self.latest_only = latest_only
        if start_url:
            self.start_url = start_url
        self.allowed_slugs = SPIDER_PARAMS[talkshow]["allowed_slugs"]
        self.allowed_domains = SPIDER_PARAMS[talkshow]["allowed_domains"]
        self.excludes = SPIDER_PARAMS[talkshow]["excludes"]
        self.recent_episodes = SPIDER_PARAMS[talkshow]["recent_episodes"]
        self.follow_cb = SPIDER_PARAMS[talkshow]["follow_cb"]
        self.output_dir = OUTPUT_DIR

    @property
    def output_path(self) -> Path:
        talkshow_dir = Path(self.output_dir / self.talkshow)
        talkshow_dir.mkdir(exist_ok=True, parents=True)
        return talkshow_dir

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any):
        episode_urls = self.recent_episodes(response)
        episode_urls = list(
            filter(lambda url: all(slug in url for slug in self.allowed_slugs), episode_urls)
        )
        episode_urls = list(dict.fromkeys(episode_urls))
        if self.excludes:
            episode_urls = list(
                filter(lambda url: all(ex not in url for ex in self.excludes), episode_urls)
            )
        if self.latest_only:
            episode_urls = [episode_urls[0]]
            print(episode_urls)
            input()
        for i, episode_url in enumerate(episode_urls):
            self.log(f"episode_urls ({i}) - {episode_url}", logging.INFO)
        cb_kwargs = {"output_path": self.output_path, "log_cb": self.log}
        yield from response.follow_all(episode_urls, callback=self.follow_cb, cb_kwargs=cb_kwargs)


class SimpleRawSpider(scrapy.Spider):
    name: str = "raw-spider"
    allowed_slugs: list[str]
    allowed_domains: list[str]

    def __init__(self, talkshow: str, start_urls: list[str], *args, **kwargs):
        super(SimpleRawSpider, self).__init__(*args, **kwargs)
        self.talkshow = talkshow
        self.start_urls = start_urls
        self.follow_cb = SPIDER_PARAMS[talkshow]["follow_cb"]
        self.output_dir = OUTPUT_DIR

    @property
    def output_path(self) -> Path:
        talkshow_dir = Path(self.output_dir / self.talkshow)
        talkshow_dir.mkdir(exist_ok=True, parents=True)
        return talkshow_dir

    def start_requests(self) -> None:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> None:
        self.log(f"response.url - {response.url}", logging.INFO)
        yield self.follow_cb(response, self.output_path, self.log)
