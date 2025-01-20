# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from datetime import datetime

from itemloaders.processors import MapCompose
from psycopg2 import sql
from psycopg2.sql import Composed
from scrapy import Item, Field


def fix_length_string(l: str) -> int:
    return int(l.strip(" min"))


def exists(l: str) -> bool:
    print(l)
    return l is not None


class IllnerEpisodeItem(Item):
    ep_table = sql.Identifier("illnerepisode")
    g_table = sql.Identifier("illnerguests")
    name = Field(output_processor=MapCompose(str.strip))
    date = Field(output_processor=MapCompose(str.strip))
    length = Field(output_processor=MapCompose(str.strip, fix_length_string))
    description = Field(output_processor=MapCompose(str.strip))
    factcheck = Field(output_processor=MapCompose(exists))
    guests = Field()


class LanzEpisodeItem(Item):
    ep_table = sql.Identifier("lanzepisode")
    g_table = sql.Identifier("lanzguests")
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

    def exists_in_database(self) -> tuple[Composed, tuple]:
        return sql.SQL("SELECT EXISTS(SELECT 1 FROM {table} WHERE name=%s)").format(
            table=self.ep_table
        ), (self["name"][0],)

    def episode_as_query(self) -> tuple[Composed, tuple]:
        date = datetime.strptime(self["date"][0], "%d.%m.%Y").strftime("%Y-%m-%d")
        return (
            sql.SQL(
                "INSERT INTO {table} (name, date, length, description) VALUES (%s, %s, %s, %s);"
            ).format(table=self.ep_table),
            (self["name"][0], date, self["length"][0], self["description"][0]),
        )

    def guests_as_query(self) -> tuple[Composed, list]:
        guests = [
            (self["name"][0], guest["name"], guest["role"], guest["text"])
            for guest in self["guests"]
        ]
        return (
            sql.SQL(
                "INSERT INTO {table} (lanzepisode_name, name, role, message) VALUES %s;"
            ).format(table=self.g_table),
            guests,
        )

    @classmethod
    def from_jsonl_entry(cls, line: str) -> "LanzEpisodeItem":
        fields = json.loads(line)
        return LanzEpisodeItem(**fields)


class EpisodeItemMI(Item): ...
