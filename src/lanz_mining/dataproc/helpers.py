from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

from lanz_mining.database.mappings import get_known_politicians
from lanz_mining.dataproc.utils import preprocess_dataframe


def find_unmapped_politicians_helper(input_file: Path) -> list[dict[str, str]]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    politicians = get_known_politicians()
    print(df[df["guest_genre"] == "Politik"][["name", "role"]])
    unknown_politicians = list(
        filter(
            lambda entry: entry[0] not in politicians,
            df[df["guest_genre"] == "Politik"][["name", "role"]].values,
        )
    )
    return unknown_politicians


def find_unmapped_roles_helper(input_file: Path) -> tuple[list[str], list]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    unmapped_guest_genre = list(set(df[df["guest_genre"] == "Other"]["role"].values))
    no_roles = df[pd.isna(df["role"])].values
    return unmapped_guest_genre, no_roles


def find_abbreviated_names(input_file: Path, search_str: Optional[str] = None) -> list[str]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    abbreviated_names = [
        name for name in df.name.unique() if any([c in name for c in ". , -".split()])
    ]
    if search_str:
        abbreviated_names = list(filter(lambda n: search_str in n, abbreviated_names))
    return abbreviated_names


def find_full_date_range(input_file: Path) -> dict[str, np.datetime64]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    return {"start": df.date.min(), "end": df.date.max()}
