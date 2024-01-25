import scrapy
from scrapy.http import Response

from lanz_mining.miner.spiders.parse import parse_item
from lanz_mining.params import URL_PREFIX


class LanzSpider(scrapy.Spider):
    name: str = "lanzspider"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = ["https://www.zdf.de/gesellschaft/markus-lanz"]

    def parse(self, response: Response, **kwargs: any) -> any:
        recent_episodes = response.xpath("//article/div/div/div/div/div/h3/a/@href").getall()
        recent_episodes = list(set(filter(lambda url: URL_PREFIX in url, recent_episodes)))
        yield from response.follow_all(recent_episodes, callback=parse_item)
