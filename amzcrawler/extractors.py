from html.parser import HTMLParser
# from helpers import enqueue_url
# from bs4 import BeautifulSoup

htmlparser = HTMLParser()

def get_title(item):
    title = item.xpath('.//h2//@data-attribute').extract_first()
    if title:
        # print(title.text.encode("utf-8"))
        return title
        # return htmlparser.unescape(title.text.encode("utf-8"))
    else:
        return "<missing product title>"


def get_url(item):
    url = item.css('.a-text-normal.s-access-detail-page').xpath('./@href').extract_first()
    if url:
        return url
    else:
        return "<missing product url>"


def get_price(item):
    # price = item.xpath('.//div/div/div/div[2]/div[3]/div[1]/div[3]/a/span[1]/span/span')
    # if price:
    #     return price
    # else:
    #     price = item.xpath('.//div/div/div/div[2]/div[3]/div[1]/div[2]/a/span/span/span')
    return None

def get_price_used(item):
    price_used = item.css('span.a-size-base.a-color-base::text').extract_first()
    if price_used:
        return float(price_used[1:]) + 3.99    # the price already include shipping
    return None

def get_price_tradein(item):
    tradein_price = item.css('span.a-color-price::text').re_first(r'\d+.\d+')
    if tradein_price:

        # for a_color_price_span in a_color_price_spans:
        #     if a_color_price_span["class"][0] == "a-size-small":
        #         continue
            
        return float(tradein_price)      # return tradein price without the $sign

    return None

def get_page_category(page):
    return page.find("title").text

def get_primary_img(item):
    thumb = item.xpath('.//img//@src').extract_first()
    if thumb:
        return thumb

    return None