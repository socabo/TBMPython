from html.parser import HTMLParser
# from helpers import enqueue_url
# from bs4 import BeautifulSoup

htmlparser = HTMLParser()


def get_sidebar_links(page):

    # https://www.amazon.com/s/ref=sr_nr_n_0?fst=as%3Aoff&rh=n%3A283155%2Ck%3Atextbook&
    #                                keywords=textbook&ie=UTF8&qid=1480598393&rnid=2941120011
    # https://www.amazon.com/gp/search/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A283155%2Ck%3Atextbook&
    #                               keywords=textbook&ie=UTF8&qid=1480598491&spIA=1451116594


    count = 0

    # look for subcategory links on this page
    #subcategories = page.findAll("div", "categoryRefinementsSection")  # downward arrow graphics
    #subcategories.extend(page.findAll("li", "sub-categories__list__item"))  # carousel hover menu
    sidebar = page.find("div", "categoryRefinementsSection")
    if sidebar:
        subcategories = sidebar.findAll("li", attrs={"class": None})  # left sidebar without 'Any Category' link

    for subcategory in subcategories:
        link = subcategory.find("a")
        if not link:
            continue
        link = link["href"]
        if link == "#":     #remove 'See More/Less' links
            continue
        count += 1
        enqueue_url(link)

    return count

def get_title(item):
    title = item.xpath('.//h2//@data-attribute').extract_first()
    if title:
        # print(title.text.encode("utf-8"))
        return title
        # return htmlparser.unescape(title.text.encode("utf-8"))
    else:
        return "<missing product title>"


def get_url(item):
    url = item.css('.s-access-detail-page').xpath('.//@href').extract_first()
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