import re
import polars as pl

from typing import Optional


def check_expertise_pre_string(string: str) -> Optional[str]:
    expertise_pattern = re.compile(r"(\w*)(expert)|((\w*)(-Expert))")
    match_grps = re.search(expertise_pattern, string)
    if match_grps:
        match_grps = [grp for grp in match_grps.groups() if grp is not None]
    else:
        return None
    return_string = match_grps[-2][:-1] if match_grps[-2].endswith("s") else match_grps[-2]
    return return_string


def check_expertise_post_string(string: str) -> Optional[str]:
    expertise_pattern = re.compile(r"[Ee]xpert(\S*) (für) ((\w* [A-Z][a-z]*)|(\w*))")
    match_grps = re.search(expertise_pattern, string)
    if match_grps:
        match_grps = [grp for grp in match_grps.groups() if grp is not None]
    else:
        return None
    return_string = match_grps[-1][:-1] if match_grps[-1].endswith("s") else match_grps[-1]
    return return_string


def get_experts_mapping(row: dict[any]) -> Optional[str]:
    """Finds an expertise for a given row by it's 'role' and 'message'"""

    def check_row(r) -> bool:
        return all([key in r for key in ["role", "message"]])

    assert check_row(row), "Expected row to have 'role' and 'message'"

    role = row["role"]
    message = row["message"]
    expertises = []
    for entry in (role, message):
        exps = [check_expertise_pre_string(entry), check_expertise_post_string(entry)]
        expertises.extend([e for e in exps if e is not None])

    return_str = None if len(expertises) == 0 else expertises[0]
    return return_str


def apply_expertise_column(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.struct("role", "message")
        .map_elements(get_experts_mapping, return_dtype=pl.String)
        .alias("expertise")
    )
