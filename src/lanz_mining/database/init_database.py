import os
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values

from lanz_mining.miner.items import EpisodeItem

create_lanzepisode_table_str = """
CREATE TABLE IF NOT EXISTS lanzepisode (
    name VARCHAR(255) PRIMARY KEY, 
    date DATE NOT NULL,
    length int,
    description text
)
"""
create_lanzguest_table_str = """
CREATE TABLE IF NOT EXISTS lanzguests (
    lanzepisode_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    message text,
    CONSTRAINT pk_episodename_name PRIMARY KEY (lanzepisode_name, name)
)
"""


def load_history_data(jsonl_file: Path) -> list[EpisodeItem]:
    return [EpisodeItem.from_jsonl_entry(line) for line in jsonl_file.open("r").readlines()]


def init_connection() -> (any, any):
    load_dotenv()  # Load environment
    try:
        conn = psycopg2.connect(  # Create/Connect to database
            host=os.getenv("DB_HOSTNAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
        )
    except psycopg2.DatabaseError as error:
        print("Unable to connect to the database")
        raise error
    cur = conn.cursor()  # Create cursor
    return conn, cur


# Copy of items.EpisodeItem.episode_as_query due to the item differences, when loading from json.
def episode2query(item) -> tuple[str, tuple]:
    date = datetime.strptime(item["date"], "%d.%m.%Y").strftime("%Y-%m-%d")
    return (
        "INSERT INTO lanzepisode (name, date, length, description) VALUES (%s, %s, %s, %s);",
        (item["name"], date, item["length"], item["description"]),
    )


# Copy of items.EpisodeItem.guests_as_query due to the item differences, when loading from json.
def guests2query(item) -> tuple[str, list]:
    guests = [
        (item["name"], guest["name"], guest["role"], guest["text"]) for guest in item["guests"]
    ]
    return (
        "INSERT INTO lanzguests (lanzepisode_name, name, role, message) VALUES %s;",
        guests,
    )


def init_data(items: list[EpisodeItem], cur, conn) -> None:
    for item in items:
        cur.execute(*episode2query(item))
        conn.commit()
        insert_query, values = guests2query(item)
        execute_values(cur, insert_query, values, template=None, page_size=20)
        conn.commit()


def main():
    items = load_history_data(Path("outputs/history/historic_items.jsonl"))
    conn, cur = init_connection()
    cur.execute(create_lanzepisode_table_str)  # Create tables, if not existing
    cur.execute(create_lanzguest_table_str)
    conn.commit()
    init_data(items, cur, conn)  # Insert all the data to database
    conn.close()


if __name__ == "__main__":
    main()
