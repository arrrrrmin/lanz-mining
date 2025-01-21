import os
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from lanz_mining.miner.items import LanzEpisodeItem


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
create_illnerepisode_table_str = """
CREATE TABLE IF NOT EXISTS illnerepisode (
    name VARCHAR(255) PRIMARY KEY, 
    date DATE NOT NULL,
    length int,
    description text,
    factcheck boolean
)
"""
create_illnerguest_table_str = """
CREATE TABLE IF NOT EXISTS illnerguests (
    illnerepisode_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    CONSTRAINT pk_illnerepisodename_name PRIMARY KEY (illnerepisode_name, name)
)
"""


def load_history_data(jsonl_file: Path) -> list[LanzEpisodeItem]:
    return [LanzEpisodeItem.from_jsonl_entry(line) for line in jsonl_file.open("r").readlines()]


def init_connection() -> (any, any):
    # Load environment variables
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOSTNAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
        )
    except psycopg2.DatabaseError as error:
        print("Unable to connect to the database")
        raise error
    # Create cursor
    cur = conn.cursor()
    # Create tables, if not existing
    cur.execute(create_lanzepisode_table_str)
    cur.execute(create_lanzguest_table_str)
    cur.execute(create_illnerepisode_table_str)
    cur.execute(create_illnerguest_table_str)
    conn.commit()
    return conn, cur


@DeprecationWarning
def episode2query(item) -> tuple[str, tuple]:
    date = datetime.strptime(item["date"], "%d.%m.%Y").strftime("%Y-%m-%d")
    return (
        "INSERT INTO lanzepisode (name, date, length, description) VALUES (%s, %s, %s, %s);",
        (item["name"], date, item["length"], item["description"]),
    )


@DeprecationWarning
def guests2query(item) -> tuple[str, list]:
    guests = [
        (item["name"], guest["name"], guest["role"], guest["text"]) for guest in item["guests"]
    ]
    return (
        "INSERT INTO lanzguests (lanzepisode_name, name, role, message) VALUES %s;",
        guests,
    )
