import scrapy
from .. import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..extractors import get_title, get_price_used, get_price_tradein, get_primary_img, get_url, get_price
from ..helpers import get_crawl_time, load_csv2db

class QuotesSpider(CrawlSpider):
    name = "tradeins"

    allowed_domains = ['www.amazon.com']
    start_urls = [ settings.start_url ]


    rules = (
        # Extract categories links
        Rule(LinkExtractor(allow=['.*ref=sr_nr_n_\d*.*']), callback='parse_item', follow=True),

        # Extract the 'next page' links 
        Rule(LinkExtractor(allow=['.*ref=sr_pg_\d*.*']), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for result in response.xpath('//li[starts-with(@id,"result_")]'):
             yield {
                        'title': get_title(result),
                        'product_url': get_url(result),
                        'listing_url': response.url,
                        'price': get_price(result),
                        'price_used': get_price_used(result),
                        'price_tradein': get_price_tradein(result),
                        'primary_img': get_primary_img(result),
                        'crawl_time': get_crawl_time(),
                    }
