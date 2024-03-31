from pathlib import Path

import pandas as pd

from lanz_mining.database.mappings import get_known_politicians
from lanz_mining.dataproc.utils import preprocess_dataframe


def find_unmapped_politicians_helper(input_file: Path) -> list[str]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    politicians = get_known_politicians()
    unknown_politicians = list(
        filter(lambda name: name not in politicians, df[df["guest_genre"] == "Politik"]["name"])
    )
    return unknown_politicians


def find_unmapped_roles_helper(input_file: Path) -> tuple[list[str], list]:
    df = pd.read_csv(input_file.open("r"), sep=",")
    df = preprocess_dataframe(df)
    unmapped_guest_genre = list(set(df[df["guest_genre"] == "Other"]["role"].values))
    no_roles = df[pd.isna(df["role"])].values
    return unmapped_guest_genre, no_roles
