from argparse import ArgumentParser, Namespace
from pathlib import Path

import polars as pl
import altair as alt

from lanz_mining.database import mappings, naming
from lanz_mining.dataproc import preprocess

# *** Constants ***


party_colors = {
    "FDP": "yellow",
    "B90G": "green",
    "LINKE": "#D60000",
    "SPD": "red",
    "CDU": "black",
    "CSU": "black",
    "Parteilos": "lightgrey",
    "Freie Wähler": "grey",
    "BSW": "purple",
    "AfD": "blue",
    None: "steelblue",
}


# *** Plotting ***


def plot_top_n_guests(df: pl.DataFrame, n: int) -> None:
    res = df["name"].value_counts().sort("count", descending=True)
    res = res[:n]

    sort = alt.EncodingSortField(field="count", op="values", order="ascending")
    x_axes = alt.X("count", title="Invitations")
    y_axes = alt.Y("name", title="Guest", sort=sort)
    plot = (
        alt.Chart(res)
        .mark_bar(cornerRadius=4)
        .encode(x=x_axes, y=y_axes)
        .properties(width=800, height=n * 20)
    )

    plot.save(f"figures/top-{n}-guests.html")


def plot_political_parties(df: pl.DataFrame) -> None:
    assert "party" in df.columns, "Party column is not existing yet."
    _df = df.with_columns(pl.col("party").replace_strict(party_colors).alias("party_color"))
    res = _df["party"].value_counts().sort("count", descending=True).drop_nulls()
    res = res.with_columns(pl.col("party").replace_strict(party_colors).alias("color"))

    sort = alt.EncodingSortField(field="count", op="values", order="ascending")
    x_axes = alt.X("party", title="Political party", sort=sort)
    y_axes = alt.Y("count", title="Invitations")
    color = alt.Color("color").scale(None).legend()
    plot = (
        alt.Chart(res)
        .mark_bar(size=40, cornerRadius=4)
        .encode(x=x_axes, y=y_axes, color=color)
        .properties(width=600, height=400)
    )

    plot.save("figures/political_parties.html")


def plot_invitations_per_newspaper(df: pl.DataFrame) -> None:
    res = df["pub_platform"].value_counts().sort("count", descending=True).drop_nulls()

    sort = alt.EncodingSortField(field="count", op="values", order="ascending")
    x_axes = alt.X("count", title="Invitations")
    y_axes = alt.Y("pub_platform", title="Affiliated news paper", sort=sort)
    plot = (
        alt.Chart(res)
        .mark_bar(cornerRadius=4)
        .encode(x=x_axes, y=y_axes)
        .properties(width=600, height=400)
    )

    plot.save(f"figures/invitations_per_publication_platform.html")


def plot_encounter_matrix_pol(df: pl.DataFrame) -> None:
    party2genres = {}
    all_genres = list(mappings.ROLE_GENRE_MAP.keys())
    self_party_index = [ind for ind, name in enumerate(all_genres) if name == "Politik"][0]
    self_party_count = []

    for i, party in enumerate(naming.ALL_PARTIES):
        episode_names = df.filter(pl.col("party") == party)["lanzepisode_name"]
        party_episodes = df.filter(pl.col("lanzepisode_name").is_in(episode_names))
        row = [
            len(party_episodes.filter(pl.col("genre") == genre)) / len(party_episodes)
            for genre in all_genres
        ]
        self_party_count.append(episode_names.len())
        row[self_party_index] -= episode_names.len() / len(party_episodes)
        party2genres[party] = row

    df_matrix = pl.DataFrame(party2genres, schema=naming.ALL_PARTIES)
    df_matrix = df_matrix.insert_column(0, pl.Series("genre", all_genres))
    df_matrix = df_matrix.unpivot(index="genre", variable_name="party")
    # Replace 0 with None to plot it in white and better indicate absence of data
    df_matrix = df_matrix.with_columns(pl.col("value").replace(0, None))
    plot = (
        alt.Chart(df_matrix)
        .mark_rect()
        .encode(
            x=alt.X("genre:N", title="Genre"),
            y=alt.Y("party:N", title="Party"),
            color=alt.Color("value:Q", title="Encounting rate"),
        )
        .properties(width=600, height=400)
    )
    plot.save(f"figures/party_encounter_matrix.html")


# *** Exploration  ***


def explore(file: Path):
    df = pl.read_csv(file.open("r"), separator=",")
    # Use episode name as date by parsing the name
    df = preprocess.default_preprocessing(df)
    plot_top_n_guests(df, 40)
    plot_political_parties(df)
    plot_invitations_per_newspaper(df)
    plot_encounter_matrix_pol(df)
    # print(df.head(25))


def call_for_args() -> Namespace:
    arg_parser = ArgumentParser("Crawling data from a history file (html search).")
    arg_parser.add_argument(
        "--file", type=Path, help="Database export file 'guests.csv'", required=True
    )
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    arguments = call_for_args()
    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        explore(file=arguments.file)
