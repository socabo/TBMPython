# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AmzcrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    product_url = Field()
    listing_url = Field()
    price = Field()
    price_used = Field()
    price_tradein = Field()
    primary_img = Field()
    crawl_time = Field()
    # pass
