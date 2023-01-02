# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#import sqlite3
import psycopg2



class AmazonscrapingPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="booksdb",
            user="testuser",
            password="postgres"
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS books_tb""")
        self.curr.execute("""create table books_tb(
                product_name text,
                product_author text,
                product_price text,
                product_imagelink text
                )""")

    def process_items(self, item, spider):
        self.curr.execute("SELECT * FROM books_tb")
        results = self.curr.fetchall()
        # Print the results to the console
        print(results)
        self.store_db(item)
        self.curr.close()
        self.conn.close()
        return item

    def store_db(self, item):
        try:
            self.curr.execute("""insert into books_tb values (%s, %s, %s, %s)""",(
                item['product_name'][0],
                item['product_author'][0],
                item['product_price'][0],
                item['product_imagelink'][0]
            ))
        except BaseException as e:
            print(e)
        self.conn.commit()



