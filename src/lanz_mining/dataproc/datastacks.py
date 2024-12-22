"""
DEPRECATED

Pandas is a deprecated dependency!
"""


import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from lanz_mining.dataproc.utils import preprocess_dataframe, preprocess_texts


def get_date(d: dict) -> str:
    return d["date"]


def get_genre(d: dict) -> str:
    return d["guest_genre"]


def get_date_year(d: dict) -> int:
    return datetime.fromisoformat(d["date"]).year


def get_json_format_date(d: str) -> str:
    return datetime.fromisoformat(d).strftime("%Y-%m-%d")


class DataStack:
    def __init__(self, input_file: Path, output_file: Path):
        self.input_file = input_file
        self.output_file = output_file
        self.df = self._read_data()
        self.json_data = {}
        self.transform()

    def _read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.input_file.open("r"), sep=",")

    def write_data(self) -> None:
        json.dump(self.json_data, self.output_file.open("w"), indent=4, ensure_ascii=False)

    def transform(self) -> None:
        raise NotImplementedError()


class GuestFrequency(DataStack):
    """Outputs a dictionary where each entry contains a guest to frequency map."""

    def __init__(self, input_file: Path, output_file: Path, top_n: int = -1):
        self.top_n = top_n if top_n > 0 else -1  # Either a valid number or all (-1)
        super(GuestFrequency, self).__init__(input_file, output_file)

    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)

        guests_freq_list = []
        for name, appearances in list(self.df.groupby("name")):
            appearances_list = json.loads(
                appearances.to_json(date_format="iso", orient="records", force_ascii=False)
            )
            all_roles, all_main_genres, all_parties = [], [], []
            for i, a in enumerate(appearances_list):
                appearances_list[i]["date"] = get_json_format_date(a["date"])
                all_roles.append(appearances_list[i]["role"])
                all_main_genres.append(appearances_list[i]["main_genre"])
                all_parties.append(appearances_list[i]["party_membership"])
            frequency = len(appearances_list)
            all_roles = list(set(all_roles))
            this_guests_freq = {
                "name": name,
                "frequency": frequency,
                "all_roles": all_roles,
                # Only one main available
                "main_genre": all_main_genres[0],
                # Choose the latest party membership when multiple
                "party_membership": all_parties[-1],
                "appearances": appearances_list,
            }
            guests_freq_list.append(this_guests_freq)
        guests_freq_list = sorted(
            guests_freq_list, key=lambda guest: guest["frequency"], reverse=True
        )
        self.json_data["guests"] = guests_freq_list[: self.top_n]
        self.json_data["time_range"] = {
            "start": self.df.date.min().strftime("%Y-%m-%d"),
            "end": self.df.date.max().strftime("%Y-%m-%d"),
        }
        self.json_data["num_episodes"] = len(self.df.lanzepisode_name.unique())
        self.json_data["num_guests"] = len(guests_freq_list)


class GuestFrequencyDist(DataStack):
    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)
        frequencies = self.df.groupby("name").count()["lanzepisode_name"]
        unique, counts = np.unique(frequencies, return_counts=True)
        self.json_data["distribution"] = [
            {"num_appearance": int(num_appearance), "num_guests": int(num_guests)}
            for num_appearance, num_guests in zip(unique, counts)
        ]


class GuestGenreByYear(DataStack):
    """Outputs and year to data dictionary based on guest genre classification."""

    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)

        data = json.loads(self.df.to_json(date_format="iso", orient="records", force_ascii=False))
        years = sorted(list(set(map(get_date_year, data))))
        yearly_data = {
            year: list(filter(lambda d: get_date_year(d) == year, data)) for year in years
        }

        for year, year_data in yearly_data.items():
            set_of_dates = list(set(map(get_date, year_data)))
            set_of_genres = list(set(map(get_genre, data)))
            # Map dates and genres to sorted inds in the later initialized matrix.
            date2inds = {d: i for i, d in enumerate(sorted(set_of_dates, reverse=True))}
            genre2inds = {g: i for i, g in enumerate(sorted(set_of_genres, reverse=False))}
            # Init a matrix of timestamps to genre (tg: time,genre).
            arr_tg = np.zeros((len(set_of_dates), len(set_of_genres)), dtype=np.int_)
            for d in year_data:
                date_ind = date2inds[get_date(d)]
                genre_ind = genre2inds[get_genre(d)]
                arr_tg[date_ind][genre_ind] += 1

            self.json_data[year] = {
                "values": arr_tg.T.tolist(),
                "genres": sorted(set_of_genres, reverse=False),
                "dates": [get_json_format_date(d) for d in sorted(set_of_dates, reverse=True)],
            }


class PoliticialPartyDist(DataStack):
    """Returns the structure to analyse political party distributions."""

    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)
        self.df = self.df[self.df.guest_genre == "Politik"]

        df_by_partymembership = self.df.groupby("party_membership")
        self.json_data = []
        for group in df_by_partymembership:
            party_dict = {
                "party": group[0],
                "details": json.loads(
                    group[1][["name", "date", "role", "message"]].to_json(
                        date_format="iso", orient="records", force_ascii=False
                    )
                ),
            }
            self.json_data.append(party_dict)


class GuestMessageDataStack(DataStack):
    """."""

    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)
        self.df = preprocess_texts(self.df)
        search = "Bildung"
        # masked_df = self.df.apply(lambda row: row.astype(str).str.contains(search).any(), axis=1)
        # print(masked_df)
        search_mask = np.array(self.df["message"].str.contains(search.lower(), regex=False))
        print(search_mask.shape)
        masked_df = self.df.loc[search_mask]
        print(masked_df)
        print(masked_df[["name", "main_genre", "message", "party_membership"]].values)
        groups = masked_df.groupby(
            ["main_genre", "party_membership"], group_keys=True, dropna=False
        )
        for group in groups:
            print(group[0], len(group[1]))


class GuestGenreDataStack(DataStack):
    """Returns the structure of the mapped guest genres."""

    def transform(self) -> None:
        self.df = preprocess_dataframe(self.df)
        genres_and_roles = list()
        for genre_name, genre_group in list(self.df.groupby("guest_genre")):
            roles_in_genre = list()
            for role_name, role_group in list(genre_group.groupby("role")):
                persons_in_role = list()
                for person_name, person_group in list(role_group.groupby("name")):
                    persons_in_role.append({"name": person_name, "value": len(person_group)})
                roles_in_genre.append({"name": role_name, "children": persons_in_role})
            genres_and_roles.append({"name": genre_name, "children": roles_in_genre})
        self.json_data = {"name": "guests", "children": genres_and_roles}
