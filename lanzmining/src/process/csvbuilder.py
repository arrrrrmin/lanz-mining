import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Callable, Union, Any, Optional

import polars as pl

from misc import Group, Episode, Guest, Entry
from process import mappings
from process.utils import requires_columns

KNOWN_POLITICIANS = mappings.get_known_politicians()


@requires_columns(["episode_name", "name"])
def named_row_index(df: pl.DataFrame, index_name: str = "named_id") -> pl.DataFrame:
    def map_fn(row: dict) -> str:
        return f"{row['episode_name']}|{row['name']}"

    return df.with_columns(
        pl.struct(["episode_name", "name"])
        .map_elements(lambda row: map_fn(row), pl.String)
        .alias(index_name)
    )


def normalize_name_str(name: str) -> str:
    """Makes strings of name column more uniform."""
    result_str = re.sub(r",(.+)*", "", name)
    result_str = re.sub(r"\((.+)", "", result_str)
    result_str = result_str.replace(".", " ")
    result_str = result_str.replace("-", " ")
    result_str = result_str.replace("  ", " ").strip()
    if result_str in mappings.NAMES_MAP.keys():
        result_str = mappings.NAMES_MAP[result_str]

    return result_str


@requires_columns("name")
def norm_names(df: pl.DataFrame) -> pl.DataFrame:
    """Normalize name column of passed dataframe."""
    return df.with_columns(
        name=pl.col("name").map_elements(normalize_name_str, pl.String)
    )


def find_party_membership(row: dict) -> Optional[str]:
    """Find party membership if one is known in the mapping.
    For complicated cases party membership depends on the date."""
    name = row["name"]
    d = row["date"]

    membership = None
    if name not in KNOWN_POLITICIANS:
        return membership
    if name in mappings.PARTY_MEMBERSHIP_MAP.keys():
        membership = mappings.PARTY_MEMBERSHIP_MAP[name]
    else:
        compilcated_membership_map = mappings.get_complicated_party_memberships()
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


@requires_columns(["role", "party", "media"])
def apply_group_affiliation(df: pl.DataFrame) -> pl.DataFrame:
    """Applies group membership, based on `role` and `party` columns"""

    def map_fn(row: dict) -> Optional[str]:
        role, party, media_institute = row["role"], row["party"], row["media"]
        if party:
            return Group.Politics
        if media_institute:
            return Group.Journalist
        if not role:
            return None
        for group_name, kw_pattern in mappings.GROUP_MAPS.items():
            match = re.search(kw_pattern, role.lower())
            if match is not None:
                return group_name
        return Group.Default

    return df.with_columns(
        pl.struct("role", "party", "media")
        .map_elements(lambda row: map_fn(row), pl.String)
        .alias("group")
    )


@requires_columns(["role", "message"])
def apply_media_institute(df: pl.DataFrame) -> pl.DataFrame:
    """Looks for the role and message to find a news paper affiliation."""

    def map_fn(row: dict) -> Optional[str]:
        role = row["role"] if row["role"] is not None else ""
        message = row["message"] if row["message"] is not None else ""

        # if group != types.Group.Journalist:
        #     return None
        found_media = []
        for media_name, kw_pattern in mappings.MEDIA_MAPS.items():
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
        pl.struct("name", "role", "message")
        .map_elements(map_fn, return_dtype=pl.String)
        .alias("media")
    )


@requires_columns(["group", "media"])
def apply_media_to_group(df: pl.DataFrame) -> pl.DataFrame:

    def map_fn(row: dict) -> str:
        group = row["group"]
        media_affiliation = row["media"]
        if group in [Group.Culture, Group.Default] and media_affiliation is not None:
            group = Group.Journalist
        return group

    return df.with_columns(
        pl.struct("group", "media")
        .map_elements(map_fn, return_dtype=pl.String)
        .alias("group")
    )


def known_keys_by_names(
    dataframe: pl.DataFrame, fill_up_key: str
) -> dict[str, Optional[str]]:
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


def check_df_file_params(file_or_df: Union[Path, pl.DataFrame]) -> bool:
    """Simle check for assertation"""
    return isinstance(file_or_df, Path) or isinstance(file_or_df, pl.DataFrame)


def init_dataframe(
    file_or_df: Union[Path, pl.DataFrame],
    merge_file: Optional[Path] = None,
) -> Union[pl.DataFrame, AssertionError]:
    """Decide if dataframe is passed or to load it from a file.
    When merge_file is passed, merge raw data with file_or_df.
    Data passed by file_or_df overwrites merge_file."""
    if isinstance(file_or_df, Path):
        file_or_df = pl.read_csv(
            file_or_df, separator=",", schema=Entry.get_polars_schema()
        )
    if merge_file is not None and merge_file.exists():
        snapshot_df = pl.read_csv(
            merge_file, separator=",", schema=Entry.get_polars_schema()
        )
        index_name = "named_id"
        file_or_df = named_row_index(file_or_df, index_name)
        snapshot_df = named_row_index(snapshot_df, index_name)
        # Exclude snapshot entries included in the current vault
        # Current vault entries are considered more recent
        snapshot_df_filtered = snapshot_df.filter(
            ~pl.col(index_name).is_in(file_or_df[index_name].to_list())
        )
        merged_df = pl.concat([snapshot_df_filtered, file_or_df]).sort(index_name)
        file_or_df = merged_df.drop(index_name)

    return file_or_df


class CSVBuilder:
    def __init__(
        self, file_or_df: Union[Path, pl.DataFrame], merge_file: Optional[Path] = None
    ):
        assert check_df_file_params(file_or_df), "Please pass either file or dataframe"
        self.dataframe = init_dataframe(file_or_df, merge_file)
        self.__add_index()
        self.processing_fns = []

        self.add_processing_fn(norm_names)
        self.add_processing_fn(apply_policial_membership)
        self.add_processing_fn(apply_media_institute)
        # Need to rework this!!
        self.add_processing_fn(apply_group_affiliation)
        self.add_processing_fn(self.__apply_gap_fillers)
        self.add_processing_fn(apply_media_to_group)

    @property
    def __get_raw_columns(self) -> list[str]:
        raw_columns = list(Episode.model_fields.keys()) + list(
            Guest.model_fields.keys()
        )
        del raw_columns[raw_columns.index("guests")]
        return raw_columns

    def __add_index(self) -> None:
        """Simple index column added to the dataframe.
        Might not be needed anymore?"""
        self.dataframe = self.dataframe.with_row_index("index")

    @requires_columns(["group", "media"])
    def __apply_gap_fillers(self, *_: tuple[Any, ...]) -> pl.DataFrame:
        """Updates 'group' and 'media' rows with low information, by majority votes of known entries."""
        self.dataframe = apply_nearest_entries(self.dataframe, "group")
        self.dataframe = apply_nearest_entries(self.dataframe, "media")
        return self.dataframe

    @requires_columns("date")
    def reduce_to_timerange(
        self, start: datetime.date, end: datetime.date = datetime.today().date()
    ) -> pl.DataFrame:
        """Reduce local frame by date range and return a copy."""
        return self.dataframe.filter(start <= pl.col("date")).filter(
            pl.col("date") < end
        )

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

    def snapshot(self, snapshot_file: Path):
        """Return the raw data from the dataframe, exluding the processed data for later usage."""
        self.dataframe[self.__get_raw_columns].write_csv(snapshot_file)
