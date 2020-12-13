from utils import crawler, scraper
from html import unescape
import re
import time

NEWEGG_URL = "https://newegg.com"
NEWEGG_RTX_PATH = "/p/pl?N=100007709%20601357282"
NEWEGG_RX_PATH = "/p/pl?N=100007709%20601359511"
NEWEGG_AMD_PATH = "/p/pl?N=100007671%2050001028%20601359163"
WEBHOOK_URL = "https://discordapp.com/api/webhooks/778423506294931478/rFcPl55WCL_y-ucIpEBekQ08xoXJhVw5GjqkoXZLPvP3PwRbTCc9y7mhdGHH6dmS-IxO"
NEWEGG_FILTERS = NEWEGG_RX_PATH,
#,NEWEGG_AMD_PATH,NEWEGG_RX_PATH
Alerted_Links= []
PerformCheckout = True
CheckoutAmount = 3


def clean_price(price):
    price_contains_numbers = bool(re.search(r'[\d+,]+(\d+)', price))
    if price_contains_numbers:
        # split the price to remove the empty space and pick the first item
        price = unescape(price).split()[0]

    return price


def get_prices(tree):
    price_selector = "//li[contains(@class, 'price-current')]"
    price_text = scraper.get_text(tree, price_selector)
    return list(map(lambda price: clean_price(price), price_text))


def get_names(tree):
    name_selector = "//div[@class='item-info']/a"
    return scraper.get_text(tree, name_selector)


def get_links(tree):
    link_selector = "//div[@class='item-info']/a"
    return scraper.get_attributes(tree, link_selector, "href")


def get_stock_information(tree):
    item_selector = "//div[@class='item-container']"
    child_selector = "div[@class='item-info']/p[contains(., 'OUT OF STOCK')]"
    stock_details = scraper.get_children_text(
        tree, item_selector, child_selector)
    # set None to in stock, handles case when item has no "out of stock" label
    return list(map(lambda element: element or "IN STOCK", stock_details))


def get_ids(tree):
    item_id_selector = "//ul[@class='item-features']/li[contains(., 'Item #')]/text()"
    return scraper.get_nodes(tree, item_id_selector)


def get_items():
     for url_filter in NEWEGG_FILTERS:
        tree = get_tree(url_filter)
        prices = get_prices(tree)
        names = get_names(tree)
        links = get_links(tree)
        ids = get_ids(tree)
        stock_details = get_stock_information(tree)
        items = []

        for index, price in enumerate(prices):
            name = names[index]
            link = links[index]
            stock = stock_details[index]
            try:
                id = ids[index]
            except:
                id = ""

            items.append({
                'name': name,
                'link': link,
                'stock': stock,
                'price': price,
                'id': id
            })

        return items

def get_link(data_rows):
    lines = []
    for data in iter(data_rows):
        if "IN STOCK" in data['stock'] and "6900" in data['name']:
            lines.append(data['link'])
    return lines



def get_tree(url_filter):
    crawl_url = f"{NEWEGG_URL}{url_filter}"
    try:
        html = crawler.crawl_html(crawl_url)
    except:
        time.sleep(10)
        get_tree(url_filter)
    html = scraper.get_tree(html)
    return html

