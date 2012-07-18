from decimal import Decimal

from bs4 import BeautifulSoup, SoupStrainer
import requests

from django.db import models
from django.core.exceptions import ValidationError


class Stock(models.Model):
    SITE_NAME_CHOICES = (
        ('iem', 'Iowa Electronic Markets'),
        ('intrade', 'Intrade'),
    )
    site = models.CharField(choices=SITE_NAME_CHOICES, max_length=7)
    intrade_id = models.IntegerField(unique=True, null=True, blank=True)
    # Not sure yet best way to identify IEM trades. Maybe an ID and group number
    symbol = models.SlugField(unique=True)
    last_trade = models.DecimalField(max_digits=3, decimal_places=3)
    bid = models.DecimalField(max_digits=3, decimal_places=3)
    ask = models.DecimalField(max_digits=3, decimal_places=3)

    def __unicode__(self):
        return '{} on {}'.format(self.symbol, self.site)

    def save(self, *args, **kwargs):
        self = self.sync()
        super(Stock, self).save(*args, **kwargs)

    def clean(self):
        #Require intrade_id if the stock is on intrade
        if self.site == 'intrade' and not self.intrade_id:
            raise ValidationError('Intrade stocks must have an ID')

    def sync(self, fields=['symbol', 'last_trade', 'bid', 'ask']):
        """
        Update specified fields in this stock from the marketplace.
        """
        if self.site == 'intrade':
            updated_fields = self.intrade_fields(self.intrade_id, fields)
        self.__dict__.update(**updated_fields)
        return self

    @staticmethod
    def intrade_fields(intrade_id, fields):
        """
        Given an intrade_id, and the fields to sync, it will return a dictionary
        of fields with their values
        """
        URL = 'http://api.intrade.com/jsp/XML/MarketData/ContractBookXML.jsp?'
        r = requests.get('{}id={}&depth=1'.format(URL, intrade_id))
        # Only parse the xml tags corresponding to the fields
        FIELD_TAGS = {
            'symbol': 'symbol',
            'last_trade': 'contractInfo',
            'bid': 'bid',
            'ask': 'offer',
        }
        # remove tags not passed
        tags = [FIELD_TAGS[field] for field in FIELD_TAGS if field in fields]
        soup = BeautifulSoup(r.text, 'xml',
                             parse_only=SoupStrainer(tags))
        returned_items = {}
        for field in fields:
            tag = soup.find(FIELD_TAGS[field])
            if field == 'symbol':
                returned_items[field] = tag.text
            elif field == 'last_trade':
                returned_items[field] = Decimal(tag['lstTrdPrc']) / Decimal(100)
            elif field == 'bid' or 'ask':
                returned_items[field] = Decimal(tag['price']) / Decimal(100)
        return returned_items


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    stocks = models.ManyToManyField(Stock, through='StockGroup')
    completion_date = models.DateField()
    greatest_difference = models.DecimalField(max_digits=3, decimal_places=3)
    apr = models.DecimalField(max_digits=5, decimal_places=5)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.sync_stocks(['bid', 'ask'])
        #self.greatest_difference = self.find_greatest_difference()
        super(Group, self).save(*args, **kwargs)

    def sync_stocks(self, *args, **kwargs):
        """
        Sync all the stocks in the group
        If 'fields' keyword is provided, will only sync those fields
        """
        for stock in self.stocks.all():
            stock.sync(*args, **kwargs)

    def find_greatest_difference(self):
        pass


class StockGroup(models.Model):
    stock = models.ForeignKey(Stock, unique=True)
    group = models.ForeignKey(Group, related_name='stock_group')
    other_side = models.BooleanField()
    lowest = models.BooleanField()
    highest = models.BooleanField()

    def save(self, *args, **kwargs):
        self.sync_stocks(['bid', 'ask'])
        super(Group, self).save(*args, **kwargs)

