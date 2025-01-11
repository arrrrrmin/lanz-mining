import polars as pl

from lanz_mining.dataproc import experts, preprocess


def test_check_expertise_pre_string():
    test_strings = ["Nahost-Experte", "Wirtschaftsexperte"]
    assert_strings = ["Nahost", "Wirtschaft"]
    for i, string in enumerate(test_strings):
        result_string = experts.check_expertise_pre_string(string)
        assert result_string == assert_strings[i]


def test_check_expertise_post_string():
    test_strings = [
        "expertin für internationale Beziehungen",
        "Expertin für künstliche Intelligenz",
        "Experte für Personalmanagement",
    ]
    assert_strings = ["internationale Beziehungen", "künstliche Intelligenz", "Personalmanagement"]
    for i, string in enumerate(test_strings):
        result_string = experts.check_expertise_post_string(string)
        assert result_string == assert_strings[i]


def test_experts(dataframe: pl.DataFrame):
    _df = preprocess.default_preprocessing(dataframe)
    _df = experts.apply_expertise_column(_df)

    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        print(_df)

    df_experts = _df.filter(pl.col("expertise").is_not_null())

    test_filter = df_experts.filter(pl.col("name") == "Alexander Graf Lambsdorff")
    assert (
        sum([expertise == "Außenpolitik" for expertise in test_filter["expertise"].to_numpy()]) >= 3
    )

    test_filter = df_experts.filter(pl.col("name") == "Linus Neumann")
    assert len(test_filter) >= 3

    test_filter = df_experts.filter(pl.col("name") == "Prof. Volker Quaschning")
    assert all([expertise == "Energie" for expertise in test_filter["expertise"].to_numpy()])
