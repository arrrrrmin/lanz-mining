import datetime
from argparse import Namespace, ArgumentParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request

from scrapy.http import TextResponse
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from lanz_mining.miner.spiders.raw_spider import SPIDER_PARAMS, OUTPUT_DIR


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from files or current start page.")
    arg_parser.add_argument(
        "-t",
        "--talkshow",
        type=str,
        help="What type of website is expect.",
        choices=list(SPIDER_PARAMS.keys()),
        required=True,
    )
    arg_parser.add_argument("--latest-only", action="store_true")
    args = arg_parser.parse_args()
    return args


def recent_default_episodes(response: TextResponse):
    return response.xpath("//a/@href").getall()


def recent_zdf_episodes(response: TextResponse) -> list[str]:
    urls = response.xpath('//*[@id="EPISODES"]/ol/li/div/div[2]/h3/a/@href').getall()
    return urls


def recent_carenmiosga_episodes(response: TextResponse, latest_only: bool = False):
    if latest_only:
        return response.xpath(
            '//*[@id="content"]/div/div[2]/div/div/div/div/div/div/div[2]/h4/a/@href'
        ).getall()
    return recent_default_episodes(response)


class Spider:
    def __init__(self, talkshow: str, latest_only: bool = False):
        self.talkshow = talkshow
        self.start_url = SPIDER_PARAMS[talkshow]["start_url"]
        self.allowed_domains = SPIDER_PARAMS[talkshow]["allowed_domains"]
        self.allowed_slugs = SPIDER_PARAMS[talkshow]["allowed_slugs"]
        self.excludes = SPIDER_PARAMS[talkshow]["excludes"]
        self.recent_episodes = SPIDER_PARAMS[talkshow]["recent_episodes"]
        self.follow_cb = SPIDER_PARAMS[talkshow]["follow_cb"]
        self.parse_fn = SPIDER_PARAMS[talkshow]["parse_fn"]
        self.latest_only = latest_only
        # Following capability is not supported somehow
        _ = DesiredCapabilities.FIREFOX.pop("moz:debuggerAddress")
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(
            service=Service(),
            options=options,
        )
        self.output_dir = OUTPUT_DIR

    @property
    def output_path(self) -> Path:
        talkshow_dir = Path(self.output_dir / self.talkshow)
        talkshow_dir.mkdir(exist_ok=True, parents=True)
        return talkshow_dir

    def run(self) -> None:
        self.driver.get(self.start_url)
        if self.talkshow in ["markuslanz", "maybritillner"]:
            WebDriverWait(self.driver, 2).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "#EPISODES"),
                )
            )

        response = TextResponse(
            url=self.start_url,
            request=Request(url=self.start_url),
            body=self.driver.page_source.encode("utf-8"),
        )

        if self.talkshow in ("markuslanz", "maybritillner"):
            urls = recent_zdf_episodes(response)
        elif self.talkshow == "carenmiosga":
            urls = recent_carenmiosga_episodes(response, self.latest_only)
        else:
            urls = recent_default_episodes(response)

        urls = list(filter(lambda u: any([slug in u for slug in self.allowed_slugs]), urls))
        if self.excludes:
            urls = list(filter(lambda u: not any([ex in u for ex in self.excludes]), urls))
        if self.talkshow == "maischberger":
            urls = sorted(urls, reverse=True)
        if self.latest_only:
            urls = urls[:1]

        for url in urls:
            query_url = "https://" + self.allowed_domains[0] + url
            self.driver.get(query_url)
            if self.talkshow in ["markuslanz", "maybritillner"]:
                WebDriverWait(self.driver, 2).until(
                    expected_conditions.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="radix-«Rl7netql5ebdnb»-content-details"]/div/div[1]')
                    )
                )
            test_response = TextResponse(
                url=query_url,
                request=Request(url=query_url),
                body=self.driver.page_source.encode("utf-8"),
            )
            if self.talkshow in ["markuslanz", "maybritillner"]:
                element = test_response.xpath(
                    '//*[@id="radix-«Rl7netql5ebdnb»-content-details"]/div/div[1]'
                ).get()
                if element is None:
                    raise ValueError(f"Required element in episode {url} is {element}")

            self.save_episode(url)
        self.driver.quit()

    def save_episode(self, url: str) -> None:
        file = urlparse(url).path.split("/")[-1]
        today = datetime.date.today().strftime("%Y-%m-%d")
        current_path = Path(self.output_path / file.rstrip(".html"))
        current_path.mkdir(exist_ok=True, parents=True)
        write_file = Path(current_path / f"{today}=index.html")
        write_file.write_bytes(self.driver.page_source.encode("utf-8"))
        print(f"write_file - {write_file}")


def main():
    args = call_for_args()
    spider = Spider(args.talkshow, args.latest_only)
    spider.run()


if __name__ == "__main__":
    main()
