from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.http import Response

from lanz_mining.miner.items import EpisodeItem
from lanz_mining.miner.spiders.parse import parse_item


class LanzDebugSpider(scrapy.Spider):
    name: str = "lanzonetimespider"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = []

    def __init__(self, target_url: str, *args: any, **kwargs: any) -> None:
        super(LanzDebugSpider, self).__init__(*args, **kwargs)
        self.target_url = target_url

    def start_requests(self) -> Request:
        r = Request(url=self.target_url, callback=self.parse)
        print(r)
        yield r

    def parse(self, response: Response, **kwargs: Any) -> EpisodeItem:
        ep_item = parse_item(response)
        print(ep_item)
        return ep_item
