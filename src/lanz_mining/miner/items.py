# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from datetime import datetime

from itemloaders.processors import MapCompose
from scrapy import Item, Field


def fix_length_string(l: str) -> int:
    return int(l.strip(" min"))


class EpisodeItemML(Item):
    ep_table = "lanzepisode"
    g_table = "lanzguests"
    name = Field(output_processor=MapCompose(str.strip))
    date = Field(output_processor=MapCompose(str.strip))
    length = Field(output_processor=MapCompose(str.strip, fix_length_string))
    description = Field(output_processor=MapCompose(str.strip))
    guests = Field()

    def as_dict(self) -> dict:
        return {
            "name": self["name"][0],
            "date": self["date"][0],
            "length": self["length"][0],
            "description": self["description"][0],
            "guests": self["guests"],
        }

    def exists_in_database(self) -> tuple[str, tuple]:
        return "SELECT EXISTS(SELECT 1 FROM %s WHERE name=%s)", (self.ep_table, self["name"][0])

    def episode_as_query(self) -> tuple[str, tuple]:
        date = datetime.strptime(self["date"][0], "%d.%m.%Y").strftime("%Y-%m-%d")
        return (
            "INSERT INTO lanzepisode (name, date, length, description) VALUES (%s, %s, %s, %s);",
            (self["name"][0], date, self["length"][0], self["description"][0]),
        )

    def guests_as_query(self) -> tuple[str, tuple]:
        guests = [
            (self["name"][0], guest["name"], guest["role"], guest["text"])
            for guest in self["guests"]
        ]
        return (
            "INSERT INTO %s (lanzepisode_name, name, role, message) VALUES %s;",
            (self.g_table, guests),
        )

    @classmethod
    def from_jsonl_entry(cls, line: str) -> "EpisodeItemML":
        fields = json.loads(line)
        return EpisodeItemML(**fields)


class EpisodeItemMI(Item): ...
