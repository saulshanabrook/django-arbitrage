import datetime

from django.db import models
from django.core.exceptions import ValidationError

from . import api


class Stock(models.Model):
    SITE_NAME_CHOICES = (
        ('iem', 'Iowa Electronic Markets'),
        ('intrade', 'Intrade'),
    )
    site = models.CharField(choices=SITE_NAME_CHOICES, max_length=7)
    intrade_id = models.IntegerField(unique=True, null=True, blank=True)
    # Not sure yet best way to identify IEM trades. Maybe an ID and group number
    symbol = models.SlugField(unique=True)
    buying = models.DecimalField(max_digits=3, decimal_places=3, null=True,
                               blank=True)
    selling = models.DecimalField(max_digits=3, decimal_places=3, null=True,
                              blank=True)

    def __unicode__(self):
        return '{} on {}'.format(self.symbol, self.site)

    def clean(self):
        #Require intrade_id if the stock is on intrade
        if self.site == 'intrade' and not self.intrade_id:
            raise ValidationError('Intrade stocks must have an ID')

    def sync(self):
        """
        Update this stock from the marketplace.
        """
        data = api.get_fields(site=self.site, site_id=self.intrade_id)
        self.symbol = data['symbol']
        self.buying = data['buying']
        self.selling = data['selling']


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    stocks = models.ManyToManyField(Stock, through='StockGroup')
    completion_date = models.DateField()

    def __unicode__(self):
        return self.name

    @property
    def highest_buy(self):
        return max(self.stockgroups.all(), key=lambda g: g.buying)

    @property
    def lowest_sell(self):
        return min(self.stockgroups.all(), key=lambda g: g.selling)

    @property
    def greatest_difference(self):
        return self.highest_buy.buying - self.lowest_sell.selling

    @property
    def apr(self):
        time_till = self.completion_date - datetime.date.today()
        return self.greatest_difference * 365 / time_till.days


class StockGroup(models.Model):
    stock = models.ForeignKey(Stock, unique=True, related_name='stockgroup')
    group = models.ForeignKey(Group, related_name='stockgroups')
    other_side = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} in {}'.format(self.stock, self.group)

    @property
    def buying(self):
        return 1 - self.stock.selling if self.other_side else self.stock.buying

    @property
    def selling(self):
        return 1 - self.stock.buying if self.other_side else self.stock.selling
