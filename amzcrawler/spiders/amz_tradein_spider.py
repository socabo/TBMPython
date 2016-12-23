import scrapy
from .. import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..extractors import get_title, get_price_used, get_price_tradein, get_primary_img, get_url, get_price
from ..helpers import get_crawl_time, load_csv2db

class QuotesSpider(CrawlSpider):
    name = "tradeins"

    good_tradeins = 0


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
            price_tradein = get_price_tradein(result)
            if price_tradein:
                price_used = get_price_used(result)

                if not price_used:
                    continue

                if (price_tradein - price_used) >= settings.good_tradein:
                    self.good_tradeins += 1
                    yield {
                        'title': get_title(result),
                        'product_url': get_url(response),
                        'listing_url': response.url,
                        'price': get_price(result),
                        'price_used': price_used,
                        'price_tradein': price_tradein,
                        'primary_img': get_primary_img(result),
                        'crawl_time': get_crawl_time(),
                    }

    def closed(self, reason):
        print('Found {} good tradeins.'.format(self.good_tradeins))
        # load_csv2db()