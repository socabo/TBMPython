import settings
import csv

import pymysql
conn=pymysql.connect(database=settings.database, host=settings.host, user=settings.user, password=settings.password, charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

# import sqlite3
# conn = sqlite3.connect('example.db')

cur = conn.cursor()


class FoundBook(object):
    """docstring for FoundBook"""
    def __init__(self, title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time):
        super(FoundBook, self).__init__()
        self.title = title
        self.product_url = product_url
        self.listing_url = listing_url
        self.price = price
        self.price_used = price_used
        self.price_tradein = price_tradein
        self.primary_img = primary_img
        self.crawl_time = crawl_time

    def __str__(self):
        return "{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.title, self.product_url, self.listing_url, self.price, self.price_used, self.price_tradein, self.primary_img, self.crawl_time)

    def save(self):
       with open(settings.temp_csv, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([self.title,
                                self.product_url,
                                self.listing_url,
                                self.price,
                                self.price_used,
                                self.price_tradein,
                                self.primary_img,
                                self.crawl_time])

        # cur.execute("INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
        #     self.title,
        #     self.product_url,
        #     self.listing_url,
        #     self.price,
        #     self.price_used,
        #     self.price_tradein,
        #     self.primary_img,
        #     self.crawl_time
        # ))
        # conn.commit()
        # return cur.fetchone()

    @classmethod
    def load_csv2db(self):
        try:
            with open(settings.temp_csv, newline='') as csvfile:
                csvfilereader = csv.reader(csvfile, delimiter='|', quotechar='"')
                sql = "INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                for line in csvfilereader:
                    # print(line[1])
                    cur.execute(sql, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

        finally:
            conn.commit()
            conn.close()


if __name__ == '__main__':

    # setup tables
    cur.execute("DROP TABLE IF EXISTS found_books")
    cur.execute("""CREATE TABLE found_books (
        id              serial PRIMARY KEY,
        title           varchar(100),
        product_url     varchar(250) NOT NULL UNIQUE,
        listing_url     varchar(250),
        price           varchar(128),
        price_used      varchar(128),
        price_tradein   varchar(128),
        primary_img     varchar(250) NOT NULL UNIQUE,
        crawl_time      timestamp
    ) 
    ENGINE=InnoDB 
    DEFAULT CHARSET=utf8 
    COLLATE=utf8_bin 
    AUTO_INCREMENT=1
    ;""")
    conn.commit()


