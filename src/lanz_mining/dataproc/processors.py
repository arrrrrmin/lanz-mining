"""Loaders are used to load up database exports and normalize values and apply preprocessing,
based on what kind of talkshow published the information.
"""

from datetime import datetime
from pathlib import Path
from typing import Callable, Union, Any

import polars as pl

from lanz_mining.dataproc.register import TalkshowRegister
from lanz_mining.dataproc.utils import requires_columns
from lanz_mining.miner.items import Episode


def check_valid_register(register: TalkshowRegister) -> bool:
    return register.get_indices() is not None


class CSVProcessor:
    def __init__(self, file: Path, register: TalkshowRegister):
        self.dataframe = pl.read_csv(file, separator=",", schema=Episode.get_schema())
        assert check_valid_register(register), "Please create a register before using it."
        self.register = register
        self.__add_index()
        self.processing_fns = []
        # Register index is applies regardless of the inherited processor
        self.add_processing_fn(self.register.apply_register_index_col)
        self.add_processing_fn(self.__apply_context)
        self.process()

    def __add_index(self) -> None:
        self.dataframe = self.dataframe.with_row_index("index")

    @requires_columns("register_index")
    def __apply_context(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        contexts = []
        for row in self.dataframe.rows(named=True):
            context_row = {
                "register_index": row["register_index"],
                **{
                    k: 1 if v >= 0.2 else 0
                    for k, v in self.register.register[row["register_index"]].items()
                },
            }
            contexts.append(context_row)

        df_contexts = pl.from_dicts(contexts)
        return self.dataframe.join(df_contexts, on="register_index", how="inner")

    def add_processing_fn(self, fn: Union[Callable, list[Callable]]) -> None:
        if isinstance(fn, list):
            self.processing_fns.extend(fn)
        else:
            self.processing_fns.append(fn)

    def process(self):
        for fn in self.processing_fns:
            self.dataframe = fn(self.dataframe)

    @requires_columns("date")
    def reduce_to_timerange(
        self, start: datetime.date, end: datetime.date = datetime.today().date()
    ) -> pl.DataFrame:
        return self.dataframe.filter(start <= pl.col("date")).filter(pl.col("date") < end)
