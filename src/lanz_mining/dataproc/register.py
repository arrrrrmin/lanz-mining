""" A register is a collection of known crawled items with it's associated classification result.
 Here I call this a context, since the zero-shot model tries to find the entries contextual
 relatedness to different topics. The sum of all topics describes the context. """

import pickle
from pathlib import Path
from typing import Optional

import polars as pl
from tqdm import tqdm

from lanz_mining.dataproc import text

Index = str
Context = dict[str, float]
Register = dict[Index, Context]


def batched_dataframe(dataframe: pl.DataFrame, batch_size: int = 32) -> list[pl.DataFrame]:
    size = dataframe.shape[0]
    if size < batch_size:
        return [dataframe]
    is_even = size % batch_size > 0
    n_batches = size // batch_size + is_even
    batches: list[pl.DataFrame] = []
    for bid in range(1, n_batches + 1):
        batch_start, batch_end = (bid - 1) * batch_size, bid * batch_size
        print(f"Current batch {batch_start} - {batch_end}")
        batch = dataframe.filter(batch_start <= pl.col("index"))
        batch = batch.filter(pl.col("index") < batch_end)
        batches.append(batch)
    return batches


class TalkshowRegister:
    def __init__(self, topics: list[str]):
        self.topics = topics
        self.register = None
        self.config = {
            "markuslanz": {
                "index_cols": ["episode_name", "name"],
                "sequence_cols": ["message", "name", "role"],
            },
            "maybritillner": {
                "index_cols": ["episode_name", "name"],
                "sequence_cols": ["description", "name", "role"],
            },
            "carenmiosga": {
                "index_cols": ["episode_name", "name"],
                "sequence_cols": ["message", "name", "role"],
            },
            "maischberger": {
                "index_cols": ["episode_name", "name"],
                "sequence_cols": ["description", "name"],
            },
            "hartaberfair": {
                "index_cols": ["episode_name", "name"],
                "sequence_cols": ["description", "name", "role"],
            },
        }
        self.seq_template = {
            "description": "Beschreibung:",
            "message": "Beschreibung:",
            "name": "Gast:",
            "role": "Rolle:",
        }

    def __get_index(self, row: dict) -> str:
        return "+".join([row[col] for col in self.config[row["talkshow"]]["index_cols"]])

    def __get_sequence(self, row: dict) -> str:
        return "; ".join(
            [
                f"{self.seq_template[col]} {row[col]}"
                for col in self.config[row["talkshow"]]["sequence_cols"]
            ]
        )

    def __compute_register(self, dataframe: pl.DataFrame) -> Register:
        classifier = text.get_classifier_pipeline()
        progress_bar = tqdm(total=len(dataframe))
        indices, results = [], []
        for row in dataframe.rows(named=True):
            batch_index = self.__get_index(row)
            batch_sequence = self.__get_sequence(row)
            result_list = text.run_pipeline(batch_sequence, classifier)

            indices.append(batch_index)
            results.extend(result_list)
            progress_bar.update(1)
        return {index: results[i] for i, index in enumerate(indices)}

    def __compare(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        print(dataframe["talkshow"].unique())
        dataframe = dataframe.with_columns(
            pl.struct(pl.all()).map_elements(self.__get_index, pl.String).alias("register_index")
        )
        return dataframe.filter(pl.col("register_index").is_in(self.get_indices()).not_())

    def __update(self, register: Register) -> None:
        for index, context in register.items():
            self.register[index] = context

    def apply_register_index_col(self, dataframe: pl.DataFrame) -> pl.DataFrame:
        return dataframe.with_columns(
            pl.struct(pl.all()).map_elements(self.__get_index, pl.String).alias("register_index")
        )

    def get_indices(self) -> Optional[list[str]]:
        if not self.register:
            return None
        return self.register.keys()

    def create(self, dataframe: pl.DataFrame) -> Register:
        self.register = self.__compute_register(dataframe)
        return self.register

    def update(self, dataframe: pl.DataFrame) -> Register:
        assert self.register, "No register computed yet."
        dataframe = self.__compare(dataframe)
        if dataframe.is_empty():
            print("No new entries found in dataframe.")
            return self.register
        print(f"Updating {dataframe.shape[0]} guest rows ...")
        register = self.__compute_register(dataframe)
        self.__update(register)
        return self.register

    def save(self, fpath: Path) -> None:
        Path(fpath.parent).mkdir(exist_ok=True, parents=True)
        pickle.dump(self, fpath.open("wb"), pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, fpath: Path) -> "TalkshowRegister":
        return pickle.load(fpath.open("rb"))
