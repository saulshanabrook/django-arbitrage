from bs4 import BeautifulSoup
import requests

from django.db import models
from django.core.exceptions import ValidationError


class Stock(models.Model):
    SITE_NAME_CHOICES = (
        ('iem', 'Iowa Electronic Markets'),
        ('intrade', 'Intrade'),
    )
    site = models.CharField(choices=SITE_NAME_CHOICES)
    intrade_id = models.IntegerField(unique=True, null=True, blank=True)
    # Not sure yet best way to identify IEM trades. Maybe an ID and group number
    symbol = models.SlugField(unique=True, editable=False)

    # Do you think that Price should be a seperate model? It will make it a
    # little harder on the admin to see the price, you will need to click on
    # seperate model. However I think it makes more sense with the data.
    # stock.bid.price and stock.bid.volume seem nicer than stock.bid_price and
    # stock.bid_volume or something like that. Without another model the bid
    # and ask fields wouldn't by DRY.

    # Fuck DRY, I think it is easier if its just all part of the model.
    bid = models.DecimalField(max_digits=3, decimal_places=3, editable=False)
    ask = models.DecimalField(max_digits=3, decimal_places=3, editable=False)
    bid_volume = models.PositiveIntegerField(editable=False)
    ask_volume = models.PositiveIntegerField(editable=False)

    def save(self):
        self.sync()

    def clean(self):
        #Require intrade_id if the stock is on intrade
        if self.site == 'intrade' and not self.intrade_id:
            raise ValidationError('Intrade stocks must have an ID')

    def sync_intrade(intrade_id):
        URL = 'http://api.intrade.com/jsp/XML/MarketData/ContractBookXML.jsp?'
        r = requests.get('{}id={}'.format(URL, intrade_id))
        soup = BeautifulSoup(r.text, 'lxml')
        contract = soup.html.body.contractbookinfo.contractinfo
        symbol = contract.symbol.text
        bid = contract.orderbook.bids.bid['price']
        ask = contract.orderbook.offers.offer['price']
        bid_volume = contract.orderbook.bids.bid['quantity']
        ask_volume = contract.orderbook.offers.offers['quantity']
        return symbol, bid, ask, bid_volume, ask_volume


    def sync(self):
        "Update this stock from the marketplace"
        if self.site == 'intrade':
            (self.symbol, self.bid, self.ask, self.bid_volume,
             self.ask_volume) = sync_intrade(self.intrade_id)


class StockGroup(models.Model):
    side_one = models.ManyToManyField(Stock, related_name='group')
    side_two = models.ManyToManyField(Stock, related_name='group')
