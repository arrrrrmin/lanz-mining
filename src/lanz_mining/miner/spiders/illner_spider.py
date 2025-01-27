import scrapy
from icecream import ic
from scrapy import Request
from scrapy.http import Response
from tqdm import tqdm

from lanz_mining.miner.items import IllnerEpisodeItem
from lanz_mining.miner.parse import parse_illner_episode


class IllnerSpider(scrapy.Spider):
    name: str = "illnerspider"
    watch_slug = "/politik/maybrit-illner/"
    excludes = ["die-maybrit-illner-fakten-box"]
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = ["https://www.zdf.de/politik/maybrit-illner/"]
    debug: bool = False

    def parse(self, response: Response, **kwargs: any) -> any:
        recent_episodes = response.xpath("//article/div/div/div/div/div/h3/a/@href").getall()
        recent_episodes = filter(lambda url: self.watch_slug in url, recent_episodes)
        recent_episodes = filter(
            lambda url: all([ex not in url for ex in self.excludes]), recent_episodes
        )
        recent_episodes = list(set(recent_episodes))
        if self.debug:
            ic(recent_episodes)
        cb_kwargs = {"debug": self.debug}
        yield from response.follow_all(
            recent_episodes, callback=parse_illner_episode, cb_kwargs=cb_kwargs
        )


class IllnerEpisodeSpider(scrapy.Spider):
    name: str = "maybritillnerspider"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = []
    debug: bool = False

    def __init__(self, paths: list[str], debug: bool, *args: any, **kwargs: any) -> None:
        super(IllnerEpisodeSpider, self).__init__(*args, **kwargs)
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

    def parse(self, response: Response, **kwargs: any) -> IllnerEpisodeItem:
        ep_item = parse_illner_episode(response, self.debug)
        return ep_item
