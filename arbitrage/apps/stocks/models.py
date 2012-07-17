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
        # If symbol already saved, don't sync that
        self = self.sync(self)
        super(Stock, self).save(*args, **kwargs)

    def clean(self):
        #Require intrade_id if the stock is on intrade
        if self.site == 'intrade' and not self.intrade_id:
            raise ValidationError('Intrade stocks must have an ID')

    @staticmethod
    def sync(self, fields=['symbol', 'last_trade', 'bid', 'ask']):
        """
        Update specified fields in this stock from the marketplace.
        """
        if self.site == 'intrade':
            updated_fields = self.intrade_fields(self.intrade_id, fields)
        self.__dict__.update(**updated_fields)
        return self

    @classmethod
    def intrade_fields(obj, intrade_id, fields):
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
                returned_items[field] = obj.string_decimal(tag['lstTrdPrc'])
            elif field == 'bid' or 'ask':
                returned_items[field] = obj.string_decimal(tag['price'])
        return returned_items

    @staticmethod
    def string_decimal(number_string):
        """
        Converts a string to a decimal number percent
        '1' -> .01
        '50' -> .50
        '100' -> 1.00
        """
        from decimal import Decimal
        return Decimal(number_string) / Decimal(100)


class StockGroup(models.Model):
    stocks = models.ManyToManyField(Stock, through='StockGroupRelationship')
    completion_date = models.DateField()


class StockGroupRelationship(models.Model):
    stock = models.ForeignKey(Stock, unique=True)
    group = models.ForeignKey(StockGroup)
    side_one = models.BooleanField()
