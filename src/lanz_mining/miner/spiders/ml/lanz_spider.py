import scrapy
from scrapy.http import Response

from lanz_mining.miner.spiders.ml.parse_ml import parse_item_ml


class LanzSpider(scrapy.Spider):
    name: str = "lanzspider"
    watch_slug = "/gesellschaft/markus-lanz/markus-lanz-vom"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = ["https://www.zdf.de/gesellschaft/markus-lanz"]
    debug: bool = False

    def __init__(self, debug: bool, *args: any, **kwargs: any) -> None:
        super(LanzSpider, self).__init__(*args, **kwargs)
        self.debug = debug

    def parse(self, response: Response, **kwargs: any) -> any:
        recent_episodes = response.xpath("//article/div/div/div/div/div/h3/a/@href").getall()
        recent_episodes = list(set(filter(lambda url: self.watch_slug in url, recent_episodes)))
        if self.debug:
            print(recent_episodes)
        cb_kwargs = {"debug": self.debug}
        yield from response.follow_all(recent_episodes, callback=parse_item_ml, cb_kwargs=cb_kwargs)
