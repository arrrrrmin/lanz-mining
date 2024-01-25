# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import json
from pathlib import Path

import psycopg2


class Episode2JsonPipeline:
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_file = self.output_path.open("w")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        output_path = settings.get("PIPELINE_OUTPUT")
        print(output_path)

        # Instantiate the pipeline with pipeline output from settings
        return cls(output_path)

    def open_spider(self, spider):
        self.output_file = open(self.output_path, "w")

    def close_spider(self, spider):
        self.output_file.close()

    def process_item(self, item, spider):
        line = json.dumps(item.as_dict(), ensure_ascii=False) + "\n"
        self.output_file.writelines([line])
        return item


class PostgresDemoPipeline:
    def __init__(self):
        ## Connection Details
        hostname = "localhost"
        username = "postgres"
        password = "*******"  # your password
        database = "quotes"

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database,
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS lanzepisode(
            name text PRIMARY KEY, 
            date DATE NOT NULL,
            length int,
            description text
        )
        """
        )
        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS lanzguests(
            id serial PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(255),
            message text,
            CONSTRAINT fk_lanzepisode_name 
            FOREIGN KEY(name) 
            REFERENCES lanzepisode(name)
        )
        """
        )

    def process_item(self, item, spider):
        return item
