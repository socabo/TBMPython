import sys
import pymysql
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from . import settings
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MySQLStorePipeline(object):
	def __init__(self):
	    self.conn = pymysql.connect(database=settings.database, host=settings.host, user=settings.user, password=settings.password, charset='utf8',
	                    cursorclass=pymysql.cursors.DictCursor)
	    self.cursor = self.conn.cursor()

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


		except MySQLError as e:
		    print('Error {}: {}'.format(e.args[0], e.args[1]))


		return item

