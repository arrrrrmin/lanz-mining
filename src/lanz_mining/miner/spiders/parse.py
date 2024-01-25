from scrapy.http import Response
from scrapy.loader import ItemLoader

from lanz_mining.miner.items import EpisodeItem


def parse_item(response: Response) -> EpisodeItem:
    details_div = '//div[@class="details cell medium-7 large-8"]'
    teaser_info_div = '/div[@class="other-infos"]/dl/dd[@class="teaser-info"]'
    loader = ItemLoader(item=EpisodeItem(), response=response)
    loader.add_xpath("name", '//h1[@id="main-content"]/text()')
    loader.add_xpath("date", f"{details_div}{teaser_info_div}[2]/text()")
    loader.add_xpath("length", f"{details_div}{teaser_info_div}[1]/text()")
    loader.add_xpath("description", f'{details_div}/p[@class="item-description"]/text()')
    guests_div = '//div[@class="b-post-content"]/div/div'
    # participants_loader = loader.nested_xpath(participants_div)

    p_texts = response.xpath(f"{guests_div}/p/text()").getall()
    all_guests = response.xpath(f"{guests_div}/p/b/text()").getall()
    if len(all_guests) < 1:
        all_guests = response.xpath(f"{guests_div}/p/strong/text()").getall()
    guests = map_guests_to_desc(all_guests, p_texts, response)
    loader.add_value("guests", guests)
    return loader.load_item()


def map_guests_to_desc(all_guests: str, texts: list[str], response: Response) -> list[dict]:
    guests = []
    for i, guest in enumerate(all_guests):
        try:
            name, role = guest.split(",")
        except ValueError as _:
            name = response.xpath('//h1[@id="main-content"]/text()').get()
            print(_)
            print(name)
            print(guest)
            name, role = guest, "None"
        try:
            text = texts[i]
        except IndexError as _:
            print(_)
            text = ""

        guests.append({"name": name.strip(), "role": role.strip(), "text": text})
    return guests
