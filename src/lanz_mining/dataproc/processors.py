"""Loaders are used to load up database exports and normalize values and apply preprocessing,
based on what kind of talkshow published the information.
"""

from datetime import datetime
from pathlib import Path
from typing import Callable, Union, Any

import polars as pl

from lanz_mining.dataproc import preprocess
from lanz_mining.dataproc.register import TalkshowRegister
from lanz_mining.dataproc.utils import requires_columns


def check_valid_register(register: TalkshowRegister) -> bool:
    return register.get_indices() is not None


class BaseProcessor:
    talkshow: str

    def __init__(self, file: Path, register: TalkshowRegister):
        self.dataframe = pl.read_csv(file, separator=",")
        assert check_valid_register(register), "Please create a register before using it."
        self.register = register
        self.__add_index()
        self.__apply_label()
        self.processing_fns = []
        # Register index is applies regardless of the inherited processor
        self.add_processing_fn(self.register.apply_register_index_col)
        self.add_processing_fn(self.__apply_context)

    def __add_index(self) -> None:
        self.dataframe = self.dataframe.with_row_index("index")

    def __apply_label(self) -> None:
        size = self.dataframe.shape[0]
        talkshow_label = pl.Series("talkshow", [self.talkshow] * size)
        self.dataframe.insert_column(-1, talkshow_label)

    @requires_columns("register_index")
    def __apply_context(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        contexts = []
        for row in self.dataframe.rows(named=True):
            context_row = {
                "register_index": row["register_index"],
                **{
                    # k: v # round(v * 100, 2)
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
        self, start: datetime, end: datetime = datetime.today()
    ) -> pl.DataFrame:
        return self.dataframe.filter(start <= pl.col("date")).filter(pl.col("date") < end)


class LanzProcessor(BaseProcessor):
    talkshow: str = "markuslanz"

    def __init__(self, file: Path, register: TalkshowRegister):
        super(LanzProcessor, self).__init__(file, register)
        self.add_processing_fn(
            [
                preprocess.fix_date_col_by_title,
                preprocess.norm_abbreviated_names,
                preprocess.apply_policial_membership,
                self.__apply_genre_affiliation,
                self.__apply_pub_platform,
            ]
        )
        self.process()

    @requires_columns(["role", "party"])
    def __apply_genre_affiliation(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "party")
            .map_elements(preprocess.find_genre_by_role_party, pl.String)
            .alias("genre")
        )

    @requires_columns(["role", "genre", "message"])
    def __apply_pub_platform(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "genre", "message")
            .map_elements(preprocess.find_pub_platform_by_role_messsage, pl.String)
            .alias("pub_platform")
        )


class IllnerProcessor(BaseProcessor):
    talkshow: str = "maybritillner"

    def __init__(self, file: Path, register: TalkshowRegister):
        super(IllnerProcessor, self).__init__(file, register)
        self.add_processing_fn(
            [
                self.__text_clearing,
                preprocess.apply_policial_membership,
                self.__apply_genre_affiliation,
                self.__apply_pub_platform,
            ]
        )
        self.process()

    @requires_columns(["name", "date", "factcheck", "description", "role"])
    def __text_clearing(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        self.dataframe = preprocess.norm_str_columns(
            self.dataframe, ["name", "description", "role"]
        )
        self.dataframe = preprocess.norm_names(self.dataframe)
        self.dataframe = preprocess.norm_abbreviated_names(self.dataframe)
        self.dataframe = preprocess.convert_date_column(self.dataframe)
        return preprocess.convert_factcheck_column(self.dataframe)

    @requires_columns(["role", "party"])
    def __apply_genre_affiliation(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "party")
            .map_elements(preprocess.find_genre_by_role_party, pl.String)
            .alias("genre")
        )

    @requires_columns(["role", "genre"])
    def __apply_pub_platform(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "genre")
            .map_elements(preprocess.find_pub_platform_by_role, pl.String)
            .alias("pub_platform")
        )


class MiosgaProcessor(BaseProcessor):
    talkshow: str = "carenmiosga"

    def __init__(self, file: Path, register: TalkshowRegister):
        super().__init__(file, register)
        self.add_processing_fn(
            [
                self.__text_clearing,
                preprocess.apply_policial_membership,
                self.__apply_genre_affiliation,
                self.__apply_pub_platform,
            ]
        )
        self.process()

    @requires_columns(["name", "date", "factcheck", "description", "role"])
    def __text_clearing(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        self.dataframe = preprocess.norm_str_columns(
            self.dataframe, ["name", "description", "role"]
        )
        self.dataframe = preprocess.norm_names(self.dataframe)
        self.dataframe = preprocess.norm_abbreviated_names(self.dataframe)
        self.dataframe = preprocess.convert_date_column(self.dataframe)
        return preprocess.convert_factcheck_column(self.dataframe)

    @requires_columns(["role", "party"])
    def __apply_genre_affiliation(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "party")
            .map_elements(preprocess.find_genre_by_role_party, pl.String)
            .alias("genre")
        )

    @requires_columns(["role", "genre", "message"])
    def __apply_pub_platform(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        return self.dataframe.with_columns(
            pl.struct("role", "genre", "message")
            .map_elements(preprocess.find_pub_platform_by_role_messsage, pl.String)
            .alias("pub_platform")
        )


class MaischProcessor(BaseProcessor):
    talkshow: str = "maischberger"

    def __init__(self, file: Path, register: TalkshowRegister):
        super().__init__(file, register)
        self.add_processing_fn(
            [
                self.__text_clearing,
                preprocess.apply_policial_membership,
            ]
        )
        self.process()

    @requires_columns(["maischepisode_name", "date", "description"])
    def __text_clearing(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        self.dataframe = preprocess.norm_str_columns(self.dataframe, ["name", "description"])
        self.dataframe = preprocess.norm_names(self.dataframe)
        self.dataframe = preprocess.norm_abbreviated_names(self.dataframe)
        return preprocess.convert_date_column(self.dataframe)
