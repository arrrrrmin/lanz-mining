import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from lanz_mining.miner.items import LanzEpisodeItem


# Tables for markuslanz
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

# Tables for maybritillner
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

# Tables for carenmiosga
create_miosgaepisode_table_str = """
CREATE TABLE IF NOT EXISTS miosgaepisode (
    name VARCHAR(255) PRIMARY KEY, 
    date DATE NOT NULL,
    description text,
    factcheck boolean
) 
"""
create_miosgaguest_table_str = """
CREATE TABLE IF NOT EXISTS miosgaguests (
    miosgaepisode_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    message text,
    CONSTRAINT pk_miosgaepisodename_name PRIMARY KEY (miosgaepisode_name, name)
)
"""

# Tables for carenmiosga
create_maischepisode_table_str = """
CREATE TABLE IF NOT EXISTS maischepisode (
    name VARCHAR(255) PRIMARY KEY, 
    date DATE NOT NULL,
    description text
) 
"""
create_maischguest_table_str = """
CREATE TABLE IF NOT EXISTS maischguests (
    maischepisode_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT maischepisode_name PRIMARY KEY (maischepisode_name, name)
)
"""


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
    cur.execute(create_miosgaepisode_table_str)
    cur.execute(create_miosgaguest_table_str)
    cur.execute(create_maischepisode_table_str)
    cur.execute(create_maischguest_table_str)
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
