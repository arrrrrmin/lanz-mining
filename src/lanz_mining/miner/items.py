# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Optional

import polars as pl


@dataclass
class Guest:
    name: str
    role: Optional[str] = None
    message: Optional[str] = None


@dataclass
class Episode:
    episode_name: str
    date: datetime.date
    description: str
    talkshow: str
    guests: list[Guest]
    factcheck: Optional[bool] = None
    length: Optional[int] = None

    def as_flat_dict(self) -> list[dict[str, Any]]:
        lines = []
        for guest in self.guests:
            episode = asdict(self)
            episode.pop("guests")
            lines.append({**episode, **asdict(guest)})
        return lines

    @staticmethod
    def get_polars_schema() -> dict:
        return {
            "episode_name": pl.String,
            "date": pl.Date,
            "description": pl.String,
            "factcheck": pl.Boolean,
            "length": pl.UInt16,
            "name": pl.String,
            "role": pl.String,
            "message": pl.String,
            "talkshow": pl.String,
        }
