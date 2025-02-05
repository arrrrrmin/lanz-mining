from datetime import datetime
from pathlib import Path

import polars as pl

from lanz_mining import params
from lanz_mining.dataproc.processors import BaseProcessor
from lanz_mining.dataproc.register import TalkshowRegister


class Parameters:
    def __init__(self, talkshow: str, data_file: Path, register_file: Path):
        self.talkshow = talkshow
        self.data_file = data_file
        self.register_file = register_file

    def get_processor(self) -> BaseProcessor:
        register = TalkshowRegister.load(self.register_file)
        processor = params.TALKSHOWS[self.talkshow]["processor"](self.data_file, register)
        return processor


def get_all_basic_frames(
    keep_cols: list[str], prefix: str = ""
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    lanz_processor: BaseProcessor = Parameters(
        "markuslanz",
        Path(f"{prefix}exports/export-lanz.csv"),
        Path(f"{prefix}outputs/register/register-markuslanz-main.pkl"),
    ).get_processor()
    illner_processor: BaseProcessor = Parameters(
        "maybritillner",
        Path(f"{prefix}exports/export-illner.csv"),
        Path(f"{prefix}outputs/register/register-maybritillner-main.pkl"),
    ).get_processor()
    miosga_processor: BaseProcessor = Parameters(
        "carenmiosga",
        Path(f"{prefix}exports/export-miosga.csv"),
        Path(f"{prefix}outputs/register/register-carenmiosga-main.pkl"),
    ).get_processor()
    lanz_df = lanz_processor.dataframe["lanzepisode_name", *keep_cols].rename(
        {"lanzepisode_name": "episode_name"}
    )
    illner_df = illner_processor.dataframe["illnerepisode_name", *keep_cols].rename(
        {"illnerepisode_name": "episode_name"}
    )
    miosga_df = miosga_processor.dataframe["miosgaepisode_name", *keep_cols].rename(
        {"miosgaepisode_name": "episode_name"}
    )
    return lanz_df, illner_df, miosga_df


def df_to_time_range(df: pl.DataFrame, start: datetime.date, end: datetime.date) -> pl.DataFrame:
    _df = df.filter(pl.col("date") > start)
    _df = _df.filter(pl.col("date") < end)
    return _df
