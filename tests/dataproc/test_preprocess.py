import datetime

import polars as pl

from lanz_mining.dataproc.mappings import roles, media
from lanz_mining.dataproc.mappings.types import Party
from lanz_mining.dataproc import preprocess
from lanz_mining.dataproc.preprocess import normalize_name_str


def test_normalize_name_str():
    names = [
        "Sabine Leutheusser-Schnarrenberger",
        "Tarek Al-Wazir",
        "Hubertus Meyer-Burckhardt",
        "Daniel Cohn-Bendit",
        "Hans-Olaf Henkel",
        "Marie-Agnes Strack-Zimmermann ",
        "Karl-Theodor zu Guttenberg",
        "M.-C. Ostermann",
        "Oliver Schmidt-Gutzat",
        "Wiebke Şahin-Schwarzweller",
        "Philippa Sigl-Glöckner",
        "Marie-Janine Calic",
        "Hamed Abdel-Samad",
        "Jan-Hendrik Goldbeck",
        "Sabine Rennefanz, Autorin und Journalistin",
        "Hermann-Josef Tenhagen",
        "Wolfgang Schmidt, SPD",
        "Jens Spahn, CDU",
        "Julia Löhr (FAZ)",
        "Sineb El-Masrar",
        "Ilko-Sascha Kowalczuk",
        "Bijan Djir-Sarai",
    ]
    for name in names:
        res = normalize_name_str(name)
        assert all([c not in res for c in ",-("])


def test_apply_policial_membership(dataframe: pl.DataFrame):
    def check_all_mapped(name: str, party: str) -> bool:
        return all(_df.filter(pl.col("name") == name)["party"] == party)  # noqa

    _df = preprocess.apply_policial_membership(dataframe)
    assert "party" in _df.columns
    assert check_all_mapped("Cem Özdemir", Party.B90G)
    assert check_all_mapped("Wolfgang Kubicki", Party.FDP)
    assert check_all_mapped("Markus Söder", Party.CSU)
    assert check_all_mapped("Friedrich Merz", Party.CDU)
    assert not check_all_mapped("Boris Palmer", Party.B90G)
    s, e = datetime.datetime(1972, 1, 1), datetime.datetime(2023, 5, 1)
    __df = _df.filter(pl.col("date").is_between(s, e))
    assert all(__df.filter(pl.col("name").str.contains("Boris Palmer"))["party"] == Party.B90G)
    s, e = datetime.datetime(2023, 5, 1), datetime.datetime.today()
    __df = _df.filter(pl.col("date").is_between(s, e))
    assert all(__df.filter(pl.col("name").str.contains("Boris Palmer"))["party"] == Party.NP)


def test_apply_genre_affiliation(dataframe: pl.DataFrame):
    _df = preprocess.apply_policial_membership(dataframe)
    _df = preprocess.apply_group_affiliation(_df)
    assert "group" in _df.columns
    group_counts = _df["group"].value_counts()["group"].drop_nulls()
    all_groups = roles.Group.properties()
    assert all([group in all_groups for group in group_counts.unique()])
    # Todo more tests


def test_apply_media_institute(dataframe: pl.DataFrame):
    dataframe = preprocess.apply_policial_membership(dataframe)
    dataframe = preprocess.apply_group_affiliation(dataframe)
    dataframe = preprocess.apply_media_institute(dataframe)
    with pl.Config(tbl_rows=-1, tbl_cols=5, fmt_str_lengths=80):
        dataframe = dataframe.filter(pl.col("group").eq("Journalismus"))
        print(dataframe["name", "media", "group"])
        print(dataframe["media"].null_count())


def test_known_keys_by_names(dataframe: pl.DataFrame):
    dataframe = preprocess.apply_policial_membership(dataframe)
    dataframe = preprocess.apply_group_affiliation(dataframe)
    name2group = preprocess.known_keys_by_names(dataframe, "group")
    assert all([value is not None for value in name2group.values()])
    dataframe = preprocess.apply_media_institute(dataframe)
    name2media = preprocess.known_keys_by_names(dataframe, "media")
    assert all([value is not None for value in name2media.values()])


def test_apply_nearest_entries(dataframe: pl.DataFrame):
    dataframe = preprocess.apply_policial_membership(dataframe)
    dataframe = preprocess.apply_group_affiliation(dataframe)
    name2group = preprocess.known_keys_by_names(dataframe, "group")
    dataframe = preprocess.apply_nearest_entries(dataframe, "group")
    all_groups = roles.Group.properties()
    for name, group in name2group.items():
        groups = dataframe.filter(pl.col("name").eq(name))["group"].to_numpy()
        for g in groups:
            if groups[0] is None:
                assert len(groups) == 1
            else:
                assert g in all_groups


def test_apply_nearest_media(dataframe: pl.DataFrame):
    dataframe = preprocess.apply_policial_membership(dataframe)
    dataframe = preprocess.apply_group_affiliation(dataframe)
    dataframe = preprocess.apply_media_institute(dataframe)
    name2group = preprocess.known_keys_by_names(dataframe, "media")
    dataframe = preprocess.apply_nearest_entries(dataframe, "media")
    all_media = media.MEDIA_MAPS.keys()
    for name, media_name in name2group.items():
        media_arr = dataframe.filter(pl.col("name").eq(name))["media"].to_numpy()
        for g in media_arr:
            if media_arr[0] is None:
                assert len(media_arr) == 1
            else:
                assert g in all_media
