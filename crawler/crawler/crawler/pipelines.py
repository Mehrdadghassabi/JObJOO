# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.log import logger
import psycopg2 as psycopg2

from crawler.utilities.Normalize import normalize_item
from crawler.utilities.configs import server_db, local_db


class CrawlerPipeline:
    def open_spider(self, spider):
        # db_config = local_db
        db_config = server_db
        self.conn = psycopg2.connect(
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"])
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        item_base_name = item.__class__.__base__.__name__.lower()

        ad_type = 'recruiment'

        normalize_item(item, ad_type)

        if self.not_exist(item['token'], ad_type):
            self.save_recruiment_data(item)

    def save_recruiment_data(self, item):
        try:
            self.cursor.execute(
                "insert into recruiment (" +
                (("token," if self.insertThis(item["token"]) else "") +
                 ("source_id," if self.insertThis(item["source_id"]) else "") +
                 ("time," if self.insertThis(item["time"]) else "") +
                 ("title," if self.insertThis(item["title"]) else "") +
                 ("category," if self.insertThis(item["category"]) else "") +
                 ("sub_category," if self.insertThis(item["sub_category"]) else "") +
                 ("province," if self.insertThis(item["province"]) else "") +
                 ("city," if self.insertThis(item["city"]) else "") +
                 ("neighbourhood," if self.insertThis(item["neighbourhood"]) else "") +
                 ("description," if self.insertThis(item["description"]) else "") +
                 ("url," if self.insertThis(item["url"]) else "") +
                 ("thumbnail," if self.insertThis(item["thumbnail"]) else "") +
                 ("education," if self.insertThis(item["education"]) else "") +
                 ("gender," if self.insertThis(item["gender"]) else "") +
                 ("salary," if self.insertThis(item["salary"]) else "") +
                 ("insurnace," if self.insertThis(item["insurnace"]) else "") +
                 ("experience," if self.insertThis(item["experience"]) else "")).strip(',') + 
                 (",cooperation" if self.insertThis(item["cooperation"]) else "") +
                ") " +
                "values (" +
                ((f"{item['token']}," if self.insertThis(item["token"]) else "") +
                 (f"{item['source_id']}," if self.insertThis(item["source_id"]) else "") +
                 (f"{item['time']}," if self.insertThis(item["time"]) else "") +
                 (f"'{item['title']}'," if self.insertThis(item["title"]) else "") +
                 (f"'{item['category']}'," if self.insertThis(item["category"]) else "") +
                 (f"'{item['sub_category']}'," if self.insertThis(item["sub_category"]) else "") +
                 (f"'{item['province']}'," if self.insertThis(item["province"]) else "") +
                 (f"'{item['city']}'," if self.insertThis(item["city"]) else "") +
                 (f"'{item['neighbourhood']}'," if self.insertThis(item["neighbourhood"]) else "") +
                 (f"'{item['description']}'," if self.insertThis(item["description"]) else "") +
                 (f"'{item['url']}'," if self.insertThis(item["url"]) else "") +
                 (f"'{item['thumbnail']}'," if self.insertThis(item["thumbnail"]) else "") +
                 (f"'{item['education']}'," if self.insertThis(item["education"]) else "") +
                 (f"'{item['gender']}'," if self.insertThis(item["gender"]) else "") +
                 (f"{item['salary']}," if self.insertThis(item["salary"]) else "") +
                 (f"'{item['insurnace']}'," if self.insertThis(item["insurnace"]) else "") +
                 (f"'{item['experience']}'," if self.insertThis(item["experience"]) else "")).strip(',') +
                 (f",'{item['cooperation']}'" if self.insertThis(item["cooperation"]) else "") +
                " )"
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.critical(f"storing recruiment failed: {e}")
        return item

    def not_exist(self, token, ad_type):
        try:
            self.cursor.execute(f"select count(token) from {ad_type} where token = CAST({token} as varchar)")
            data = self.cursor.fetchall()
            if int(data[0][0]) > 0:
                return False
        except Exception as e:
            self.conn.rollback()
            logger.critical(f"pipeline => not_exist: {e}")
        return True

    def insertThis(self, v):
        return str(v) != '-1' and v != 'not_defined' and v != 'notdefined' and v != 'not defined' and str(v) != '-1.0' and v != 'not-defined' \
               and v != 'NOTDEFINED' and v != 'NOT DEFINED' and len(str(v)) != 0 and v is not None
    
