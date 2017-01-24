import pymysql
from pymysql import MySQLError
from . import settings
from scrapy.exceptions import DropItem
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
from twisted.enterprise import adbapi

from pydispatch import dispatcher
from scrapy import signals
from .helpers import send_sms_report
import logging

log = logging.getLogger('pipeline')

class TradeinPricePipeline(object):

    def process_item(self, item, spider):
        if item['price_tradein']:
	        if item['price_used']:
	        	if (item['price_tradein'] - item['price_used']) >= settings.profit_per_book:
	        		return item
        else:
            raise DropItem("Missing tradein price.")


# class MySQLStorePipeline(object):
# 	def __init__(self):
# 		self.conn = pymysql.connect(database=settings.database, host=settings.host, user=settings.user, password=settings.password, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
# 		self.cursor = self.conn.cursor()
# 		self.good_tradeins = 0

# 	def process_item(self, item, spider):
# 		try:
# 			self.cursor.execute("INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
# 			    item['title'],
# 				item['product_url'],
# 			    item['listing_url'],
# 			    item['price'],
# 			    item['price_used'],
# 			    item['price_tradein'],
# 			    item['primary_img'],
# 			    item['crawl_time']
# 		    ))
	        
# 			self.conn.commit()

# 			self.good_tradeins += 1


# 		except MySQLError as e:
# 		    print('Error {}: {}'.format(e.args[0], e.args[1]))

# 		except TypeError: 
# 			pass

# 		return item

# 	def close_spider(self, spider):
# 		print('Found {} good tradeins.'.format(self.good_tradeins))
# 		# print('Found {} good tradeins.'.format(self.stats.get_value('database/items_added')))




class MySQLStorePipeline(object):

	@classmethod
	def from_crawler(cls, crawler):
	    return cls(crawler.stats)

	def __init__(self, stats):
		# self.good_tradeins = 0
	    #Instantiate DB
	    self.dbpool = adbapi.ConnectionPool ('pymysql',
	    	database=settings.database, 
	    	host=settings.host, 
	    	user=settings.user, 
	    	password=settings.password,
	        charset='utf8',
	        use_unicode = True,
	        cursorclass=pymysql.cursors.DictCursor
	    )
	    self.stats = stats
	    dispatcher.connect(self.spider_closed, signals.spider_closed)

	def spider_closed(self, spider):
		""" Cleanup function, called after crawing has finished to close open
		objects.
		Close ConnectionPool. """
		self.dbpool.close()
		crawl_duration = self.stats.get_value('finish_time') -self.stats.get_value('start_time')
		pages_per_second = self.stats.get_value('downloader/response_count')/crawl_duration.total_seconds()

		print('Found %s good tradeins in %s. Crawled %.3f pages/second.' % (self.stats.get_value('database/items_added'), crawl_duration, pages_per_second))
		
		if settings.send_sms_report:
			send_sms_report(self.stats.get_value('database/items_added'), crawl_duration, pages_per_second)

	def process_item(self, item, spider):
		if not item:
			return
		query = self.dbpool.runInteraction(self._insert_record, item)
		query.addErrback(self._handle_error)
		return item

	def _insert_record(self, tx, item):
		try:
			result = tx.execute("INSERT INTO found_books (title, product_url, listing_url, price, price_used, price_tradein, primary_img, crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
				    item['title'],
					item['product_url'],
				    item['listing_url'],
				    item['price'],
				    item['price_used'],
				    item['price_tradein'],
				    item['primary_img'],
				    item['crawl_time']
			    ))
			if result > 0:
				self.stats.inc_value('database/items_added')

		except MySQLError as e:
			print('Error {}: {}'.format(e.args[0], e.args[1]))

		except TypeError:
			pass

	def _handle_error(self, e):
	    log.error(e)