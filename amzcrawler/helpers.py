from . import settings
import csv
from datetime import datetime

import pymysql
conn=pymysql.connect(database=settings.database, host=settings.host, user=settings.user, password=settings.password, charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)

# import sqlite3
# conn = sqlite3.connect('example.db')

cur = conn.cursor()

def send_sms_report(good_tradein_count):
    
    client = Client(settings.account_sid, settings.auth_token)

    message = client.messages.create(to=settings.to_number, from_=settings.from_number,
                                         body="Done. Found {} good tradeins.".format(good_tradein_count))


def load_csv2db():
    try:
        with open(settings.temp_csv, newline='') as csvfile:
            csvfilereader = csv.reader(csvfile, delimiter=',', quotechar='"')
            sql = "INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            for line in csvfilereader:
                # print(settings.current_dir)
                if len(line) == settings.num_csv_columns:
                    cur.execute(sql, (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))

    finally:
        conn.commit()
        conn.close()
        print('CSV file loaded.')


def get_crawl_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # get datetime and convert it to a understadeble MySQL format

if __name__ == '__main__':
    # load_csv2db()
    pass