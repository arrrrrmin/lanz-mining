import datetime
import re
from typing import Optional

from icecream import ic

from scrapy.http import Response

from lanz_mining.miner.items import Guest, Episode


def fix_length_string(s: str) -> int:
    return int(s.strip(" min"))


def uniform_date_col(s: str) -> Optional[datetime.date]:
    d, m, y = s.split(".")
    date = None
    if any([_ is None for _ in (d, m, y)]):
        return date
    if len(y) == 2:
        date = datetime.datetime.strptime(s, "%d.%m.%y").date()
    elif len(y) == 4:
        date = datetime.datetime.strptime(s, "%d.%m.%Y").date()
    return date


def match_datestr(l: str, ny_digits: int = 2, no_fallback: bool = False) -> Optional[str]:
    assert ny_digits in (2, 4), "Date match only supports 2 or 4 digits."
    pattern = r"\d{2}\.\d{2}\.\d{2}" if ny_digits == 2 else r"\d{2}\.\d{2}\.\d{4}"
    year_format = "%y" if ny_digits == 2 else "%Y"
    m = re.search(pattern, l)
    if not m or not m.group(0):
        if not no_fallback:
            # Fallback to today, when there's no day to match
            return datetime.datetime.now().strftime(f"%d.%m.%Y")
        else:
            return None
    d = datetime.datetime.strptime(m.group(0), f"%d.%m.{year_format}")
    return datetime.datetime(d.year, d.month, d.day).strftime("%d.%m.%Y")


def parse_maisch_episode(response: Response, debug: bool) -> Episode:
    def match_guests(ls: list[str]) -> list[str]:
        ls = list(map(lambda _: _.replace("\xa0", ""), ls))
        guest_names = []
        for l in ls:
            names = re.search(r"(.+)[(|]", l)
            if names and names.group(1):
                names = names.group(1).replace(" und ", ", ")
                names = [
                    re.search(r"(.+) \(", n).group(1) if "(" in n else n for n in names.split(", ")
                ]
                guest_names.extend(names)
        return list(set(guest_names))

    talkshow = "maischberger"
    episode_name = response.xpath(
        "/html/body/div[3]/div/div[2]/div[1]/div/div/div/div/h1/text()"
    ).get()
    # Check uniquness of 'name'
    date = match_datestr(episode_name, 4, True)
    if date is None:
        date_text = (
            response.xpath('//*[@id="content"]/div/div[3]/div[1]/div/div[3]/p/text()').get().strip()
        )
        date = match_datestr(date_text, 2, True)
        episode_name = f"{episode_name} vom {date}"

    date = uniform_date_col(date)
    length = 75
    # //*[@id="content"]/div/div[2]/div[1]/div/div/div/div/p
    description = (
        response.xpath("/html/body/div[3]/div/div[2]/div[1]/div/div/div/div/p/text()")
        .getall()
    )
    description = " ".join([d.strip().replace("\xa0", " ") for d in description[:-1]])
    guest_sections = response.xpath(
        '//div/div/div/div/div[@class="mediaCon mediaTop small"]/div/div/span/text()'
    ).getall()[1:]
    guests = match_guests(guest_sections)
    guests = list(map(lambda name: Guest(name), guests))

    episode = Episode(episode_name, date, description, talkshow, guests=guests, length=length)
    if debug:
        ic(episode)
    return episode


def parse_miosga_episode(response: Response, debug: bool) -> Episode:
    def drop_nbsps(l: str) -> str:
        return l.replace("\xa0", " ")

    def handle_guest_infoline(l: str) -> tuple[str, str]:
        # Case one: "Annalena Baerbock (Bundesministerin des Auswärtigen, Grüne) | ..."
        # Case two: "Bijan Djir-Sarai, FDP-Generalsekretär | ..."
        # Case three: "Marie-A. Strack-Zimmermann, Vorsitzende des Verteidigungsausschusses (FDP) | ..."
        l = re.sub(r"(\W\|\WBild:)\W(.+)", "", l)
        brackets_match = re.search(r"\((.+)\)", l)
        if brackets_match is not None and len(brackets_match.group(1)) > 5:
            name_pattern = re.search(r"(.+) \(", l)
            role_pattern = re.search(r"\((.+)\)", l)
            n = drop_nbsps(name_pattern.group(1))
            r = drop_nbsps(role_pattern.group(1))
        else:
            infoline = drop_nbsps(l).split("|")[0].strip()
            info_split = infoline.split(",")
            n = info_split[0].strip()
            r = info_split[1].strip() if len(info_split) > 1 else None
        return n, r

    talkshow = "carenmiosga"
    container_path = '//div[@class="mod modA modParagraph"]/div/div[@class="box"]'
    episode_name = response.xpath(f"{container_path}/h1/text()").get().strip()
    date = match_datestr(
        response.xpath('//div[@class="section sectionC"]/div/div/div[@class="text"]/p/text()')
        .get()
        .strip()
    )
    date = uniform_date_col(date)
    description = drop_nbsps(
        response.xpath(
            '//div[@class="mediaCon mediaTop small"]//following-sibling::p[1]/text()'
        ).get()
    )
    length = 60
    factcheck = response.xpath(f'{container_path}/div/div/img[@alt="Nachgehakt"]').get() is not None
    g_infos = response.xpath(
        '//div[@class="mediaCon mediaLeft small"]/div/div/span/text()'
    ).getall()
    g_texts = response.xpath(
        '//div[@class="mediaCon mediaLeft small"]/following-sibling::p[1]/text()'
    ).getall()
    # Fallback
    if len(g_infos) == 0:
        g_infos = response.xpath(
            '//h2/preceding-sibling::div[@class="mediaCon mediaTop small"]/div/div/span/text()'
        ).getall()
        g_texts = response.xpath(
            '//div[@class="mediaCon mediaTop small"]/following-sibling::p[1]/text()'
        ).getall()
    guests = []
    for i, guest_info in enumerate(g_infos):
        name, role = handle_guest_infoline(guest_info)
        # Stupid exceptions due to a stupid CMS usage:
        skip_names = ["Zur Sendung", "Caren Miosga"]
        if any([sn in name for sn in skip_names]):
            # Skip in case factcheck is same structure as guest infos ::facepalm::
            continue
        text = drop_nbsps(g_texts[i]) if len(g_texts) == len(g_infos) else None
        guest = Guest(name, role, text)
        guests.append(guest)
    episode = Episode(
        episode_name, date, description, talkshow, factcheck=factcheck, guests=guests, length=length
    )
    if debug:
        ic(episode)
    return episode


def parse_illner_episode(response: Response, debug: bool) -> Episode:
    details_div = '//div[@class="details cell medium-7 large-8"]'
    teaser_info_div = '/div[@class="other-infos"]/dl/dd[@class="teaser-info"]'
    episode_name = response.xpath('//h1[@id="main-content"]/text()').get().strip()
    date = response.xpath(f"{details_div}{teaser_info_div}[2]/text()").get().strip()
    date = uniform_date_col(date)
    length = fix_length_string(response.xpath(f"{details_div}{teaser_info_div}[1]/text()").get())
    description = response.xpath(f'{details_div}/p[@class="item-description"]/text()').get().strip()
    factcheck = (
        response.xpath(
            f'//div[@class="b-post-content"]/section[@class="b-group-contentbox"]/div/div/h3/text()'
        ).get()
        is not None
    )
    extended_desc = get_illner_extended_decription(response).strip()
    description += f" {extended_desc}"
    talkshow = "maybritillner"
    names = response.xpath('//div[@class="guest-text"]/h3/button/text()').getall()
    roles = response.xpath('//div[@class="guest-text"]/div/p/text()').getall()
    guests: list[Guest] = []
    for i, n in enumerate(names):
        existing_names = list(map(lambda g: g.name, guests))
        if n.strip() in existing_names:
            # Fixes a rare issue, where an episode is split into two parts and
            # guests appear in both parts, which would cause trouble with p_keys in psql.
            continue
        r = roles[i] if i <= len(roles) else None  # Just in case
        if "(" in n:
            r_appendix = re.match(r"\((.+)\)|,\W(.+)", n)
            if r_appendix is not None:
                r += " ".join(r_appendix.groups()).strip()
            n = re.sub(r"\((.+)\)|,\W(.+)", "", n).strip()
        guest = Guest(n.strip(), r.strip())
        guests.append(guest)

    episode = Episode(
        episode_name, date, description, talkshow, factcheck=factcheck, length=length, guests=guests
    )

    if debug:
        ic(episode)
    return episode


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


def parse_lanz_episode(response: Response, debug: bool) -> Episode:
    details_div = '//div[@class="details cell medium-7 large-8"]'
    teaser_info_div = '/div/dl/dd[@class="teaser-info"]'

    talkshow = "markuslanz"
    length = response.xpath(f"{details_div}{teaser_info_div}[1]/text()").get()
    length = fix_length_string(length)
    episode_name = response.xpath('//h1[@id="main-content"]/text()').get().strip()
    date = response.xpath(f"{details_div}{teaser_info_div}[2]/text()").get().strip()
    date = uniform_date_col(date)
    description = response.xpath(f'{details_div}/p[@class="item-description"]/text()').get().strip()
    factcheck = False

    guests_div = '//div[@class="b-post-content"]/div/div'
    all_guests = response.xpath('//div[@class="b-post-content"]/div/div/p/b/text()').getall()
    if len(all_guests) < 1:
        all_guests = response.xpath(
            '//div[@class="b-post-content"]/div/div/p/strong/text()'
        ).getall()
    guest_messages = response.xpath(f"{guests_div}/p/text()").getall()
    guest_messages = [
        gm.strip() for gm in guest_messages if len(gm.strip()) > 0
    ]  # remove empty sets of random artifacts
    guests = map_lanz_guests(all_guests, guest_messages)
    episode = Episode(
        episode_name, date, description, talkshow, factcheck=factcheck, length=length, guests=guests
    )
    if debug:
        ic(episode)
    return episode


def map_lanz_guests(all_guests: str, texts: list[str]) -> list[Guest]:
    guests = []
    for i, guest in enumerate(all_guests):
        values = guest.split(",")
        name = values[0]
        role = values[1] if len(values) > 1 else ""
        text = texts[i] if i < len(texts) else ""
        guest = Guest(name.strip(), role.strip(), text)
        guests.append(guest)
    return guests
