from decimal import Decimal

from bs4 import BeautifulSoup, SoupStrainer
from django.core.exceptions import ValidationError
import requests


def get_fields(site, *args, **kwargs):
    if site == 'intrade':
        intrade_fields = {
            'symbol': 'symbol',
            'bid': 'buying',
            'offer': 'selling',
        }
        data = get_intrade_fields(*args, **kwargs)
        return {intrade_fields[k]: v for k, v in data.iteritems()}


def get_intrade_fields(site_id, fields=['symbol', 'bid', 'offer']):
    """
    Given an intrade_id, and the fields to sync, it will return a dictionary
    of fields with their values
    """
    URL = 'http://api.intrade.com/jsp/XML/MarketData/ContractBookXML.jsp'
    r = requests.get('{}?id={}&depth=1'.format(URL, site_id))

    #Make sure that it can retrieve stock
    error_soup = BeautifulSoup(r.text, 'xml', parse_only=SoupStrainer('error'))
    if error_soup.error:
        raise ValidationError("Cannot retrieve stock: {}".format(error_soup.error.string))

    soup = BeautifulSoup(r.text, 'xml', parse_only=SoupStrainer(fields))
    returned_items = {}
    for field in fields:
        tag = soup.find(field)
        if field == 'symbol':
            returned_items['symbol'] = tag.text
        elif field == 'bid' or 'ask':
            returned_items[field] = Decimal(tag['price']) / Decimal(100)
    return returned_items
