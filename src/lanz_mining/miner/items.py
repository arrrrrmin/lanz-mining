# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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
            "guests": self["guests"]
        }
