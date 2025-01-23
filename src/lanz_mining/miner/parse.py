import datetime
import re

from icecream import ic

from scrapy.http import Response
from scrapy.loader import ItemLoader

from lanz_mining.miner.items import LanzEpisodeItem, IllnerEpisodeItem, MiosgaEpisodeItem


def match_datestr(l: str) -> str:
    m = re.search(r"\d{2}\.\d{2}\.\d{2}", l)
    if not m.group(0):
        # Fallback to today, when there's no day to match
        return datetime.datetime.now().strftime("%d.%m.%Y")
    d = datetime.datetime.strptime(m.group(0), "%d.%m.%y")
    return datetime.datetime(d.year, d.month, d.day).strftime("%d.%m.%Y")


def parse_miosga_episode(response: Response, debug: bool) -> MiosgaEpisodeItem:
    def drop_nbsps(l: str) -> str:
        return l.replace("\xa0", " ")

    def handle_guest_infoline(l: str) -> tuple[str, str]:
        # Case one: "Annalena Baerbock (Bundesministerin des Auswärtigen, Grüne) | ..."
        # Case two: "Bijan Djir-Sarai, FDP-Generalsekretär | ..."
        # Case three: "Marie-A. Strack-Zimmermann, Vorsitzende des Verteidigungsausschusses (FDP) | ..."
        brackets_match = re.search(r"\((.+)\)", l)
        if brackets_match is not None and len(brackets_match.group(1)) > 5:
            name_pattern = re.search(r"(.+) \(", l)
            role_pattern = re.search(r"\((.+)\)", l)
            name = drop_nbsps(name_pattern.group(1))
            role = drop_nbsps(role_pattern.group(1))
        else:
            infoline = drop_nbsps(l).split("|")[0].strip()
            info_split = infoline.split(",")
            name = info_split[0].strip()
            role = info_split[1].strip() if len(info_split) > 1 else None
        return name, role

    container_path = '//div[@class="mod modA modParagraph"]/div/div[@class="box"]'
    name_select = f"{container_path}/h1/text()"
    date_select = '//div[@class="section sectionC"]/div/div/div[@class="text"]/p/text()'
    desc_select = '//div[@class="mediaCon mediaTop small"]//following-sibling::p[1]/text()'
    factcheck_select = f'{container_path}/div/div/img[@alt="Nachgehakt"]'
    date = match_datestr(response.xpath(date_select).get())
    description = drop_nbsps(response.xpath(desc_select).get())
    factcheck = response.xpath(factcheck_select).get() is not None
    g_infos_select = '//div[@class="mediaCon mediaLeft small"]/div/div/span/text()'
    g_texts_select = '//div[@class="mediaCon mediaLeft small"]/following-sibling::p[1]/text()'
    g_infos = response.xpath(g_infos_select).getall()
    g_texts = response.xpath(g_texts_select).getall()
    # Fallback
    if len(g_infos) == 0:
        g_infos_select = (
            '//h2/preceding-sibling::div[@class="mediaCon mediaTop small"]/div/div/span/text()'
        )
        g_texts_select = '//div[@class="mediaCon mediaTop small"]/following-sibling::p[1]/text()'
        g_infos = response.xpath(g_infos_select).getall()
        g_texts = response.xpath(g_texts_select).getall()
    guests = []
    for i, guest_info in enumerate(g_infos):
        guest_name, guest_role = handle_guest_infoline(guest_info)
        # Stupid exceptions due to a stupid CMS usage:
        skip_names = ["Zur Sendung", "Caren Miosga"]
        if any([sn in guest_name for sn in skip_names]):
            # Skip in case factcheck is same structure as guest infos ::facepalm::
            continue
        guest_text = drop_nbsps(g_texts[i]) if len(g_texts) == len(g_infos) else None
        guests.append({"name": guest_name, "role": guest_role, "text": guest_text})
    loader = ItemLoader(item=MiosgaEpisodeItem(), response=response)
    loader.add_xpath("name", name_select)
    loader.add_value("date", date)
    loader.add_value("description", description)
    loader.add_value("factcheck", factcheck)
    loader.add_value("guests", guests)
    item = loader.load_item()
    if debug:
        ic(item)
    return item


def parse_illner_episode(response: Response, debug: bool) -> IllnerEpisodeItem:
    details_div = '//div[@class="details cell medium-7 large-8"]'
    teaser_info_div = '/div[@class="other-infos"]/dl/dd[@class="teaser-info"]'
    name_select = '//h1[@id="main-content"]/text()'
    date_select = f"{details_div}{teaser_info_div}[2]/text()"
    length_select = f"{details_div}{teaser_info_div}[1]/text()"
    description_select = f'{details_div}/p[@class="item-description"]/text()'
    factcheck_select = (
        f'//div[@class="b-post-content"]/section[@class="b-group-contentbox"]/div/div/h3/text()'
    )

    loader = ItemLoader(item=IllnerEpisodeItem(), response=response)
    loader.add_xpath("name", name_select)
    loader.add_xpath("date", date_select)
    loader.add_xpath("length", length_select)
    description = response.xpath(description_select).get().strip()
    extended_desc = get_illner_extended_decription(response).strip()
    description += f" {extended_desc}"
    loader.add_value("description", description)
    factcheck = response.xpath(factcheck_select).get()
    loader.add_value("factcheck", factcheck is not None)
    names = response.xpath('//div[@class="guest-text"]/h3/button/text()').getall()
    roles = response.xpath('//div[@class="guest-text"]/div/p/text()').getall()
    guests: list[dict] = []
    for i, n in enumerate(names):
        existing_names = list(map(lambda g: g["name"], guests))
        if n.strip() in existing_names:
            # Fixes a rare issue, where an episode is split into two parts and
            # guests appear in both parts, which would cause trouble with p_keys in psql.
            continue
        r = roles[i] if i <= len(roles) else None  # Just in case
        guests.append({"name": n.strip(), "role": r.strip()})

    loader.add_value("guests", guests)
    item = loader.load_item()
    if debug:
        ic(item.as_dict())
    return item


def get_illner_extended_decription(response: Response) -> str:
    description_extend_select = f'//div[@class="b-post-content"]/div/div/p/text()'
    extended_desc = []
    for p in response.xpath(description_extend_select).getall():
        if '"maybrit illner"' not in p:
            extended_desc.append(p)
        else:
            # Need to stop, beacuse we hit autogenerated content.
            break
    return " ".join(extended_desc)


def parse_lanz_episode(response: Response, debug: bool) -> LanzEpisodeItem:
    details_div = '//div[@class="details cell medium-7 large-8"]'
    teaser_info_div = '/div[@class="other-infos"]/dl/dd[@class="teaser-info"]'
    loader = ItemLoader(item=LanzEpisodeItem(), response=response)
    loader.add_xpath("name", '//h1[@id="main-content"]/text()')
    loader.add_xpath("date", f"{details_div}{teaser_info_div}[2]/text()")
    loader.add_xpath("length", f"{details_div}{teaser_info_div}[1]/text()")
    loader.add_xpath("description", f'{details_div}/p[@class="item-description"]/text()')
    guests_div = '//div[@class="b-post-content"]/div/div'

    p_texts = response.xpath(f"{guests_div}/p/text()").getall()
    p_texts = [  # remove empty sets of random artifacts
        pt.strip() for pt in p_texts if len(pt.strip()) > 0
    ]
    all_guests = response.xpath(f"{guests_div}/p/b/text()").getall()
    if len(all_guests) < 1:
        all_guests = response.xpath(f"{guests_div}/p/strong/text()").getall()
    guests = map_lanz_guests(all_guests, p_texts, response)
    loader.add_value("guests", guests)
    item = loader.load_item()
    if debug:
        print(item)
    return item


def map_lanz_guests(all_guests: str, texts: list[str], response: Response) -> list[dict]:
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
