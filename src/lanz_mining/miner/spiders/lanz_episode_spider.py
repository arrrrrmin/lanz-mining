from pathlib import Path

import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader
from tqdm import tqdm

from lanz_mining.miner.items import EpisodeItem
from lanz_mining.miner.spiders.parse import parse_item


class LanzEpisodeSpider(scrapy.Spider):
    name: str = "lanzepisodespider"
    allowed_domains: list[str] = ["www.zdf.de"]
    start_urls: list[str] = []

    def __init__(self, paths: list[str], output_path: str, *args: any, **kwargs: any) -> None:
        super(LanzEpisodeSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://{self.allowed_domains[0]}{url}" for url in paths]
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def start_requests(self):
        num_urls = len(self.start_urls)
        pbar = tqdm(total=num_urls, desc="Processing")
        for i, url in enumerate(self.start_urls):
            pbar.set_description(f"Processing {i+1}/{num_urls}")
            r = Request(url=url, callback=self.parse)
            pbar.update(1)
            yield r

    def parse(self, response: Response, **kwargs: any) -> EpisodeItem:
        return parse_item(response)
