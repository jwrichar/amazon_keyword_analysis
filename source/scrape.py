from bs4 import BeautifulSoup
import requests


URL_PREFIX = 'http://amazon.com/dp/ASIN/'

HEADERS = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': ('Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/51.0.2704.64 Safari/537.36'),
    'accept': ('text/html,application/xhtml+xml,application/xml;'
               'q=0.9,image/webp,image/apng,*/*;'
               'q=0.8,application/signed-exchange;v=b3;q=0.9'),
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}


def get_product_info(asin):
    '''
    Return the info for an Amazon product as found on its
    product page.

    :param asin: str, ASIN of an amazon product

    :return: dict with the following keys:
        * title: product title (string)
        * category: product category (string)
        * features: product features (string)
    '''
    return parse_product_info(get_product_page(asin))


def get_product_page(asin):
    '''
    Scrape the product details from an Amazon product page
    given the ASIN of the product

    :param asin: str, ASIN of an amazon product

    :return: output from requests (or None if )
    '''

    print('Retrieving product info for ASIN = %s' % asin)

    url = '%s%s' % (URL_PREFIX, asin)

    page = requests.get(url, headers=HEADERS)

    # Simple check to check if page was blocked (Usually 503)
    if page.status_code != 200:
        print("Page '%s' not retrieved. Status code: %d" %
              (url, page.status_code))
        return None

    return page


def parse_product_info(page):
    '''
    Parse out information from the Amazon product page.

    :param page: page information, as returned by requests.get()

    :return: dict with the following keys:
        * title: product title (string)
        * category: product category (string)
        * features: product features (string)
    '''
    print('Parsing product details')
    # Parse out page content as xml
    soup = BeautifulSoup(page.content, features="lxml")

    # Product title
    title = soup.select("#productTitle")[0].get_text().strip()

    # Product category (concatenated)
    cats = soup.select('#wayfinding-breadcrumbs_container ul.a-unordered-list')
    if cats:
        category = ' '.join([elem.get_text().strip()
                             for elem in cats[0].findAll('li')])
    else:
        category = ''

    # Product features (concatenated)
    features = '\n'.join([elem.get_text().strip()
                          for elem in soup.select(
                         '#feature-bullets ul.a-unordered-list'
                         )[0].findAll('li')])

    return {'title': title,
            'category': category,
            'features': features}
