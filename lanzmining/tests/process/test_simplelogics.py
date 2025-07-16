import polars as pl


def test_merge_dataframe_logic():
    a = pl.DataFrame({"id": [1, 2, 3, 4], "value": ["a", "b", "c", "d"]})
    b = pl.DataFrame({"id": [2, 4], "value": ["B", "D"]})
    key = "id"
    a_filtered = a.filter(~pl.col(key).is_in(b[key].to_list()))
    result = pl.concat([a_filtered, b]).sort(key)
    assert result.rows()[1] == (2, 'B')
    assert result.rows()[3] == (4, 'D')


def test_unique_index_logic():

    def map_fn(row: dict) -> str:
        return f"{row['id']}{row['value']}"

    a = pl.DataFrame({"id": [1, 2, 3, 4], "value": ["a", "b", "c", "d"]})
    a = a.with_columns(
        pl.struct(["id", "value"])
        .map_elements(lambda row: map_fn(row), pl.String)
        .alias("id")
    )
    assert a["id"].to_list() == ["1a", "2b", "3c", "4d"]
