# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import json
from pathlib import Path

from psycopg2.extras import execute_values

from lanz_mining.database.init_database import init_connection


class Episode2JsonPipeline:
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_file = self.output_path.open("w")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        output_path = settings.get("PIPELINE_OUTPUT")
        return cls(output_path)  # Init with pipeline output from settings

    def open_spider(self, spider):  # noqa
        self.output_file = open(self.output_path, "w")

    def close_spider(self, spider):  # noqa
        self.output_file.close()

    def process_item(self, item, spider):  # noqa
        line = json.dumps(item.as_dict(), ensure_ascii=False) + "\n"
        self.output_file.writelines([line])
        return item


class DatabasePipeline:
    def __init__(self):
        self.conn, self.cur = init_connection()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):  # noqa
        self.cur.execute(*item.exists_in_database())
        self.conn.commit()
        item_exists = self.cur.fetchone()[0]
        if not item_exists:
            self.cur.execute(*item.episode_as_query())
            self.conn.commit()
            insert_query, values = item.guests_as_query()
            execute_values(self.cur, insert_query, values, template=None, page_size=20)
            self.conn.commit()
        return item
