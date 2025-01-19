from pathlib import Path

import scrapy
from scrapy.http import Request, Response
from tqdm import tqdm

from lanz_mining.miner.items import EpisodeItemML
from lanz_mining.miner.spiders.ml.parse_ml import parse_item_ml


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

    def parse(self, response: Response, **kwargs: any) -> EpisodeItemML:
        ep_item = parse_item_ml(response, self.debug)
        return ep_item
