"""Loaders are used to load up database exports and normalize values and apply preprocessing,
based on what kind of talkshow published the information.
"""

import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Callable, Union, Any, Optional

import polars as pl

from lanz_mining.dataproc.mappings import media, types, roles, politics
from lanz_mining.dataproc.mappings.names import NAMES_MAP
from lanz_mining.dataproc.register import TalkshowRegister
from lanz_mining.dataproc.utils import requires_columns
from lanz_mining.miner.items import Episode


KNOWN_POLITICIANS = politics.get_known_politicians()


def normalize_name_str(name: str) -> str:
    """Makes strings of name column more uniform."""
    result_str = re.sub(",(.+)*", "", name)
    result_str = re.sub("\((.+)", "", result_str)
    result_str = result_str.replace(".", " ")
    result_str = result_str.replace("-", " ")
    result_str = result_str.replace("  ", " ").strip()
    if result_str in NAMES_MAP.keys():
        result_str = NAMES_MAP[result_str]

    return result_str


@requires_columns("name")
def norm_names(df: pl.DataFrame) -> pl.DataFrame:
    """Normalize name column of passed dataframe."""
    return df.with_columns(name=pl.col("name").map_elements(normalize_name_str, pl.String))


def find_party_membership(row: dict) -> Optional[str]:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    name = row["name"]
    d = row["date"]

    membership = None
    if name not in KNOWN_POLITICIANS:
        return membership
    if name in politics.PARTY_MEMBERSHIP_MAP.keys():
        membership = politics.PARTY_MEMBERSHIP_MAP[name]
    else:
        compilcated_membership_map = politics.get_complicated_party_memberships()
        if name in compilcated_membership_map.keys():
            membership_ranges = compilcated_membership_map[name]
            for start, end, party in membership_ranges:
                start = datetime.strptime(start, "%Y-%m-%d").date()
                end = datetime.strptime(end, "%Y-%m-%d").date()
                if start <= d < end:
                    membership = party
                    break

    return membership


@requires_columns(["name", "date"])
def apply_policial_membership(df: pl.DataFrame) -> pl.DataFrame:
    """Applies party membership, based on `name` and `date` columns"""
    return df.with_columns(
        pl.struct("name", "date")
        .map_elements(find_party_membership, return_dtype=pl.String)
        .alias("party")
    )


@requires_columns(["role", "party"])
def apply_group_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    """Applies group membership, based on `role` and `party` columns"""

    def map_fn(row: dict) -> Optional[str]:
        role, party = row["role"], row["party"]
        if party:
            return types.Group.Politics
        if not role:
            return None
        for group_name, kw_pattern in roles.GROUP_MAPS.items():
            match = re.search(kw_pattern, role.lower())
            if match is not None:
                return group_name
        return types.Group.OptOut

    return df.with_columns(
        pl.struct("role", "party").map_elements(lambda row: map_fn(row), pl.String).alias("group")
    )


@requires_columns(["role", "message", "group"])
def apply_media_institute(df: pl.DataFrame) -> pl.DataFrame:
    """Looks for the role and message to find a news paper affiliation."""

    def map_fn(row: dict) -> Optional[str]:
        role = row["role"] if row["role"] is not None else ""
        message = row["message"] if row["message"] is not None else ""
        group = row["group"]

        if group != types.Group.Journalist:
            return None
        found_media = []
        for media_name, kw_pattern in media.MEDIA_MAPS.items():
            # Announced roles should be taken for media befound is's found in texts
            role_match = re.search(kw_pattern, role.lower())
            if role_match is not None:
                # Role matches are valued higher (append two times, for later counting)
                found_media.extend([media_name, media_name])
            message_match = re.search(kw_pattern, message.lower())
            if message_match is not None:
                found_media.append(media_name)
        # Majority vote for most often found media institute (slow but precise)
        media_counts: list[tuple[str, int]] = Counter(found_media).most_common(3)
        result_media = media_counts[0][0] if media_counts else None
        return result_media

    return df.with_columns(
        pl.struct("name", "role", "message", "group")
        .map_elements(map_fn, return_dtype=pl.String)
        .alias("media")
    )


def known_keys_by_names(dataframe: pl.DataFrame, fill_up_key: str) -> dict[str, Optional[str]]:
    """Maps column information name2information, by majority voting."""
    # TODO: Catch scenarios where guest has ambiguous key information!!!
    name2main = {}
    for name, data_group in dataframe.group_by("name"):
        name: str = name[0]
        values = (
            data_group[fill_up_key]
            .value_counts()
            .sort("count", descending=True)
            .drop_nulls()[fill_up_key]
            .to_numpy()
        )
        # Implicite None only for names without any group assignment at all
        if len(values) > 0:
            name2main[name] = values[0]
    return name2main


@requires_columns(["name"])
def apply_nearest_entries(df: pl.DataFrame, fill_up_key: str) -> pl.DataFrame:
    """Maps missing column information by looking for known entries by name."""

    def map_fn(row: dict, lookup: dict[str, str], lookup_key: str) -> Optional[str]:
        value = row[lookup_key]
        if not value and row["name"] in lookup.keys():
            value = lookup[row["name"]]
        return value

    name2group = known_keys_by_names(df, fill_up_key)
    return df.with_columns(
        pl.struct("name", fill_up_key)
        .map_elements(lambda row: map_fn(row, name2group, fill_up_key), pl.String)
        .alias(fill_up_key)
    )


def check_valid_register(register: TalkshowRegister) -> bool:
    """Simle check for assertation"""
    return register.get_indices() is not None


def check_df_file_params(file_or_df: Union[Path, pl.DataFrame]) -> bool:
    """Simle check for assertation"""
    return isinstance(file_or_df, Path) or isinstance(file_or_df, pl.DataFrame)


def init_dataframe(file_or_df: Union[Path, pl.DataFrame]) -> Union[pl.DataFrame, AssertionError]:
    """Decide if dataframe is passed or to load it from a file."""
    if isinstance(file_or_df, Path):
        return pl.read_csv(file_or_df, separator=",", schema=Episode.get_polars_schema())
    return file_or_df


class CSVProcessor:
    def __init__(
        self,
        file_or_df: Union[Path, pl.DataFrame],
        register: TalkshowRegister,
    ):
        assert check_df_file_params(file_or_df), "Please pass either file or dataframe"
        assert check_valid_register(register), "Please create a register before using it."
        self.dataframe = init_dataframe(file_or_df)
        self.register = register
        self.__add_index()
        self.processing_fns = []

        self.add_processing_fn(norm_names)
        self.add_processing_fn(self.register.apply_register_index_col)
        self.add_processing_fn(self.__apply_context)
        self.add_processing_fn(apply_policial_membership)
        self.add_processing_fn(apply_group_affiliation)
        self.add_processing_fn(apply_media_institute)
        self.add_processing_fn(self.__apply_gap_fillers)
        self.process()

    def __add_index(self) -> None:
        """Simple index column added to the dataframe.
        Might not be needed anymore?"""
        self.dataframe = self.dataframe.with_row_index("index")

    @requires_columns("register_index")
    def __apply_context(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        """Applies zsi context values, known by the reigster."""
        contexts = []
        for row in self.dataframe.rows(named=True):
            context_row = {
                "register_index": row["register_index"],
                **{
                    k: 1 if v >= 0.2 else 0  # threshold zero-shot inferenced probs
                    for k, v in self.register.register[row["register_index"]].items()
                },
            }
            contexts.append(context_row)

        df_contexts = pl.from_dicts(contexts)
        return self.dataframe.join(df_contexts, on="register_index", how="inner")

    @requires_columns(["group", "media"])
    def __apply_gap_fillers(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        """Updates 'group' and 'media' rows with low information, by majority votes of known entries."""
        self.dataframe = apply_nearest_entries(self.dataframe, "group")
        self.dataframe = apply_nearest_entries(self.dataframe, "media")
        return self.dataframe

    def add_processing_fn(self, fn: Union[Callable, list[Callable]]) -> None:
        """Add a function to the processing pipeline."""
        if isinstance(fn, list):
            self.processing_fns.extend(fn)
        else:
            self.processing_fns.append(fn)

    def process(self):
        """Run all added processing function in the pipeline."""
        for fn in self.processing_fns:
            self.dataframe = fn(self.dataframe)

    @requires_columns("date")
    def reduce_to_timerange(
        self, start: datetime.date, end: datetime.date = datetime.today().date()
    ) -> pl.DataFrame:
        """Reduce local frame by date range and return a copy."""
        return self.dataframe.filter(start <= pl.col("date")).filter(pl.col("date") < end)
