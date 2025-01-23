from typing import Any

import scrapy
from scrapy import Request
from scrapy.http import Response
from tqdm import tqdm

from lanz_mining.miner.items import MiosgaEpisodeItem
from lanz_mining.miner.parse import parse_miosga_episode


class MiosgaSpider(scrapy.Spider):
    name: str = "miosgaspider"
    watch_slug = "/caren-miosga/sendung/"  # exclude /videos/
    exclude_slug = "/videos/web-only"
    allowed_domains: list[str] = ["www.daserste.de"]
    start_urls: list[str] = ["https://www.daserste.de/information/talk/caren-miosga/"]
    crawl_first: bool = False
    debug: bool = False

    def __init__(self, crawl_first: bool, debug: bool, *args: any, **kwargs: any) -> None:
        super(MiosgaSpider, self).__init__(*args, **kwargs)
        self.crawl_first = crawl_first
        self.debug = debug

    def parse(self, response: Response, **kwargs: Any) -> Any:
        ep_xpath = response.xpath('//div[@class="box"]/div/div/div/a[@class="mediaLink"]/@href')
        recent_episodes = ep_xpath.getall()
        if self.crawl_first:
            # Just because we can, we'll take the first three items in case they are published at once
            recent_episodes = recent_episodes[:3]
        else:
            recent_episodes = list(
                set(
                    filter(
                        lambda url: self.watch_slug in url and self.exclude_slug not in url,
                        recent_episodes,
                    )
                )
            )
        if self.debug:
            print(recent_episodes)
        cb_kwargs = {"debug": self.debug}
        yield from response.follow_all(
            recent_episodes, callback=parse_miosga_episode, cb_kwargs=cb_kwargs
        )


class MiosgaEpisodeSpider(scrapy.Spider):
    name: str = "lanzepisodespider"
    allowed_domains: list[str] = ["www.daserste.de"]
    start_urls: list[str] = []
    debug: bool = False

    def __init__(self, paths: list[str], debug: bool, *args: any, **kwargs: any) -> None:
        super(MiosgaEpisodeSpider, self).__init__(*args, **kwargs)
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

    def parse(self, response: Response, **kwargs: any) -> MiosgaEpisodeItem:
        ep_item = parse_miosga_episode(response, self.debug)
        return ep_item
