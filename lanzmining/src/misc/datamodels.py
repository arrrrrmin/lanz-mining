import datetime
from pathlib import Path
from typing import Optional, Any, Mapping

from polars import DataType
from polars.datatypes import DataTypeClass
from typing_extensions import Self

import polars as pl

from pydantic import BaseModel, model_validator, HttpUrl


class Entry(BaseModel):
    episode_name: str
    date: datetime.date
    description: str
    talkshow: str
    src: str
    factcheck: Optional[bool] = None
    length: Optional[int] = None
    # A single guests info
    name: str
    role: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def get_polars_schema() -> Mapping[str, DataTypeClass | DataType]:
        return {
            "episode_name": pl.String,
            "date": pl.Date,
            "description": pl.String,
            "talkshow": pl.String,
            "src": pl.String,
            "factcheck": pl.Boolean,
            "length": pl.UInt16,
            # A single guests info
            "name": pl.String,
            "role": pl.String,
            "message": pl.String,
        }


class Guest(BaseModel):
    name: str
    role: Optional[str] = None
    message: Optional[str] = None


class Episode(BaseModel):
    episode_name: str
    date: datetime.date
    description: str
    talkshow: str
    src: HttpUrl
    guests: list[Guest]
    factcheck: Optional[bool] = None
    length: Optional[int] = None

    def as_flat_dict(self) -> list[dict[str, Any]]:
        episode = self.model_dump()
        episode["src"] = str(episode["src"])
        episode.pop("guests")
        entries: list[Entry] = [
            Entry(**episode, **guest.model_dump())
            for guest in self.guests
        ]
        return [e.model_dump() for e in entries]


class VaultConfig(BaseModel):
    markuslanz: Path
    maybritillner: Path
    maischberger: Path
    hartaberfair: Path
    carenmiosga: Path

    @staticmethod
    def is_directory(att: str, p: str | Path) -> Path or ValueError:
        p = Path(p) if not isinstance(p, Path) else p
        if not p.is_dir():
            print(f"Some paths in passed config cause problems:")
            print(f"Attribute '{att}', path '{p}' is not a dir.")
            exit(1)
        return p

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        self.is_directory("markuslanz", self.markuslanz)
        self.is_directory("maybritillner", self.maybritillner)
        self.is_directory("maischberger", self.maischberger)
        self.is_directory("hartaberfair", self.hartaberfair)
        self.is_directory("carenmiosga", self.carenmiosga)
        return self
