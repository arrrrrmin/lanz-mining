import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from lanz_mining.dataproc.utils import preprocess_dataframe


get_date = lambda d: d["date"]
get_genre = lambda d: d["guest_genre"]
get_date_year = lambda d: datetime.fromisoformat(get_date(d)).year


class DataStack:
    def read_data(self) -> None:
        raise NotImplementedError()

    def write_data(self) -> None:
        raise NotImplementedError()

    def transform(self) -> None:
        raise NotImplementedError()


class GuestGenreByYear(DataStack):
    """Outputs and year to data dictionary based on guest genre classification."""

    def __init__(self, input_file: Path, output_file: Path):
        self.input_file = input_file
        self.output_file = output_file
        self.json_data = {}
        self.df = self.read_data()
        self.transform()
        self.write_data()

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.input_file.open("r"), sep=",")

    def write_data(self) -> None:
        json.dump(self.json_data, self.output_file.open("w"), indent=4, ensure_ascii=False)

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
                "dates": [
                    datetime.fromisoformat(d).strftime("%Y-%m-%d")
                    for d in sorted(set_of_dates, reverse=True)
                ],
            }


class GuestGenreDataStack(DataStack):
    """Returns the structure of the mapped guest genres."""

    def __init__(self, input_file: Path, output_file: Path):
        self.input_file = input_file
        self.output_file = output_file
        self.json_data = {}
        self.df = self.read_data()
        self.transform()
        self.write_data()

    def read_data(self) -> pd.DataFrame:
        return pd.read_csv(self.input_file.open("r"), sep=",")

    def write_data(self) -> None:
        json.dump(self.json_data, self.output_file.open("w"), indent=4, ensure_ascii=False)

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
