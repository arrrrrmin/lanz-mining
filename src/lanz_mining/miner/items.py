# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import json
from datetime import datetime

from itemloaders.processors import MapCompose
from psycopg2 import sql
from psycopg2.sql import Composed
from scrapy import Item, Field


def fix_length_string(l: str) -> int:
    return int(l.strip(" min"))


def field_exists(l: str) -> bool:
    return l is not None


def cleanup_name(l: str) -> str:
    if "(" in l:
        grps = re.match(r"(.+)\(", l).groups()
        return grps[0].strip()
    else:
        return l


class MiosgaEpisodeItem(Item):
    ep_table = sql.Identifier("miosgaepisode")
    g_table = sql.Identifier("miosgaguests")
    name = Field(output_processor=MapCompose(str.strip))
    date = Field(output_processor=MapCompose(str.strip))
    description = Field(output_processor=MapCompose(str.strip))
    factcheck = Field()
    guests = Field()

    def as_dict(self):
        return {
            "name": self["name"][0],
            "date": self["date"][0],
            "description": self["description"][0] if "description" in self.keys() else None,
            "factcheck": self["factcheck"][0] if "factcheck" in self.keys() else None,
            "guests": self["guests"] if "guests" in self.keys() else None,
        }

    def exists_in_database(self) -> tuple[Composed, tuple]:
        return sql.SQL("SELECT EXISTS(SELECT 1 FROM {table} WHERE name=%s)").format(
            table=self.ep_table
        ), (self["name"][0],)

    def episode_as_query(self) -> tuple[Composed, tuple]:
        date = datetime.strptime(self["date"][0], "%d.%m.%Y").strftime("%Y-%m-%d")
        return (
            sql.SQL(
                "INSERT INTO {table} (name, date, description, factcheck) VALUES (%s, %s, %s, %s);"
            ).format(table=self.ep_table),
            (self["name"][0], date, self["description"][0], self["factcheck"][0]),
        )

    def guests_as_query(self) -> tuple[Composed, list]:
        guests = [
            (self["name"][0], guest["name"], guest["role"], guest["text"])
            for guest in self["guests"]
        ]
        return (
            sql.SQL(
                "INSERT INTO {table} (miosgaepisode_name, name, role, message) VALUES %s;"
            ).format(table=self.g_table),
            guests,
        )


class IllnerEpisodeItem(Item):
    ep_table = sql.Identifier("illnerepisode")
    g_table = sql.Identifier("illnerguests")
    name = Field(output_processor=MapCompose(str.strip))
    date = Field(output_processor=MapCompose(str.strip))
    length = Field(output_processor=MapCompose(str.strip, fix_length_string))
    description = Field(output_processor=MapCompose(str.strip))
    factcheck = Field()
    guests = Field()

    def as_dict(self) -> dict:
        return {
            "name": self["name"][0],
            "date": self["date"][0],
            "length": self["length"][0],
            "description": self["description"][0] if "description" in self.keys() else None,
            "factcheck": self["factcheck"][0] if "factcheck" in self.keys() else None,
            "guests": self["guests"] if "guests" in self.keys() else None,
        }

    def exists_in_database(self) -> tuple[Composed, tuple]:
        return sql.SQL("SELECT EXISTS(SELECT 1 FROM {table} WHERE name=%s)").format(
            table=self.ep_table
        ), (self["name"][0],)

    def episode_as_query(self) -> tuple[Composed, tuple]:
        date = datetime.strptime(self["date"][0], "%d.%m.%Y").strftime("%Y-%m-%d")
        return (
            sql.SQL(
                "INSERT INTO {table} (name, date, length, description, factcheck) VALUES (%s, %s, %s, %s, %s);"
            ).format(table=self.ep_table),
            (
                self["name"][0],
                date,
                self["length"][0],
                self["description"][0],
                self["factcheck"][0],
            ),
        )

    def guests_as_query(self) -> tuple[Composed, list]:
        guests = [(self["name"][0], guest["name"], guest["role"]) for guest in self["guests"]]
        return (
            sql.SQL("INSERT INTO {table} (illnerepisode_name, name, role) VALUES %s;").format(
                table=self.g_table
            ),
            guests,
        )


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
            "description": self["description"][0] if "description" in self.keys() else None,
            "guests": self["guests"] if "guests" in self.keys() else None,
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
