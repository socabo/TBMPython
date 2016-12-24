import pymysql
from pymysql import MySQLError
from . import settings
from scrapy.exceptions import DropItem
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TradeinPricePipeline(object):

    def process_item(self, item, spider):
        if item['price_tradein']:
	        if item['price_used']:
	        	if (item['price_tradein'] - item['price_used']) >= settings.good_tradein:
	        		return item
        else:
            raise DropItem("Missing tradein price.")


class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(database=settings.database, host=settings.host, user=settings.user, password=settings.password, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()
		self.good_tradeins = 0

	def process_item(self, item, spider):
		try:
			self.cursor.execute("INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
			    item['title'],
				item['product_url'],
			    item['listing_url'],
			    item['price'],
			    item['price_used'],
			    item['price_tradein'],
			    item['primary_img'],
			    item['crawl_time']
		    ))
	        
			self.conn.commit()

			self.good_tradeins += 1


		except MySQLError as e:
		    print('Error {}: {}'.format(e.args[0], e.args[1]))

		except TypeError: 
			pass

		return item

	def close_spider(self, spider):
		print('Found {} good tradeins.'.format(self.good_tradeins))