import scrapy
from icecream import ic
from scrapy import Request
from scrapy.http import Response
from tqdm import tqdm

from lanz_mining.miner.items import LanzEpisodeItem
from lanz_mining.miner.parse import parse_lanz_episode


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
            ic(recent_episodes)
        cb_kwargs = {"debug": self.debug}
        yield from response.follow_all(
            recent_episodes, callback=parse_lanz_episode, cb_kwargs=cb_kwargs
        )


class LanzEpisodeSpider(scrapy.Spider):
    name: str = "lanzepisodespider"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = []
    debug: bool = False

    def __init__(self, paths: list[str], debug: bool, *args: any, **kwargs: any) -> None:
        super(LanzEpisodeSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://{self.allowed_domains[0]}{url}" for url in paths]
        self.debug = debug

    def start_requests(self):
        num_urls = len(self.start_urls)
        pbar = tqdm(total=num_urls, desc="Processing")
        for i, url in enumerate(self.start_urls):
            pbar.set_description(f"Processing {i+1}/{num_urls}")
            r = Request(url=url, callback=self.parse)
            pbar.update(1)
            yield r

    def parse(self, response: Response, **kwargs: any) -> LanzEpisodeItem:
        ep_item = parse_lanz_episode(response, self.debug)
        return ep_item
