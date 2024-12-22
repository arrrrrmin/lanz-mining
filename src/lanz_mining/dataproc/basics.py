import polars as pl

from lanz_mining.dataproc import preprocess


def main():
    file = "exports/guests.csv"
    df = preprocess.default_preprocessing(pl.read_csv(file))
    time_range = (
        df["date"].min().strftime("%d.%m.%Y"),
        df["date"].max().strftime("%d.%m.%Y"),
    )
    num_episodes = df["lanzepisode_name"].unique().len()
    num_guests = df["name"].unique().len()
    num_genres = df["genre"].unique().len()
    genre_counts = df["genre"].value_counts().sort("count", descending=True)
    party_counts = df["party"].value_counts().drop_nulls().sort("count", descending=True)
    print("Time range:", time_range)
    print("Number of episodes:", num_episodes)
    print("Number of guests", num_guests)
    print("Number of genres", num_genres)
    print("All genres:", genre_counts)
    print("All political parties:", party_counts)


if __name__ == "__main__":  #
    with pl.Config(tbl_cols=-1, tbl_rows=-1):
        main()
