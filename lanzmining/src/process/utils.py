from typing import Union, Callable

import polars as pl


def check_columns_exist(df: pl.DataFrame, required_cols: Union[list[str], str]) -> bool:
    """Check if passed dataframe has all required columns."""
    if isinstance(required_cols, str):
        required_cols = [required_cols]
    return all([col in df.columns for col in required_cols])


def check_key_exists(row: dict, required_keys: Union[list[str], str]) -> bool:
    """Check if keys exist in the passed row dictionary."""
    return all([key in row for key in required_keys])


def requires_columns(columns: Union[list[str], str]):
    """Asserts all required columns exist in the passed dataframe (first arg) or the self.dataframe
    parameter of processor objects."""

    def _requires_columns(f: Callable):
        def wrapper(self, *args, **kwargs):
            if not isinstance(self, pl.DataFrame):
                assert_msg = f"Function '{f}' requires columns '{columns}', got {self.dataframe.columns}"
                assert check_columns_exist(self.dataframe, columns), assert_msg
            else:
                df = self
                assert_msg = (
                    f"Function '{f}' requires columns '{columns}', got {df.columns}"
                )
                assert check_columns_exist(df, columns), assert_msg
            return f(self, *args, **kwargs)

        return wrapper

    return _requires_columns


def requires_keys(keys: Union[list[str], str]):
    """Asserts all expected keys are passed in a row mapping function."""

    def _requires_keys(f: callable):
        def wrapper(row: dict):
            assert_msg = (
                f"Function '{f}' requires a row dict with {keys}, got {row.keys()}"
            )
            assert check_key_exists(row, keys), assert_msg
            return f(row)

        return wrapper

    return _requires_keys
