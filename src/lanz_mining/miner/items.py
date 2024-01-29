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


class EpisodeItem(Item):
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

    def episode_as_query(self) -> tuple[str, tuple]:
        date = datetime.strptime(self["date"][0], "%d.%m.%Y").strftime("%Y-%m-%d")
        return (
            "INSERT INTO lanzepisode (name, date, length, description) VALUES (%s, %s, %s, %s);",
            (self["name"][0], date, self["length"][0], self["description"][0]),
        )

    def guests_as_query(self) -> tuple[str, list]:
        guests = [
            (self["name"][0], guest["name"], guest["role"], guest["text"])
            for guest in self["guests"]
        ]
        return (
            "INSERT INTO lanzguests (lanzepisode_name, name, role, message) VALUES %s;",
            guests,
        )

    @classmethod
    def from_jsonl_entry(cls, line: str) -> "EpisodeItem":
        fields = json.loads(line)
        return EpisodeItem(**fields)
