import datetime
import random
from decimal import Decimal

import factory

from django.db.models import Max

from arbitrage.apps.stocks.models import Stock, Group, StockGroup


class DjangoFactory(factory.Factory):
    'Base factory to use next available id in sequence'
    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls):
        return (cls._associated_class.objects.aggregate(Max('id')).values()[0] or 0) + 1


class StockFactory(DjangoFactory):
    FACTORY_FOR = Stock


class ObamaStockIntradeFactory(StockFactory):
    site = 'intrade'
    intrade_id = 743474  # Obama vs Romney


class RandomStockFactory(StockFactory):
    site = 'intrade'
    intrade_id = factory.Sequence(lambda n: n)
    symbol = factory.Sequence(lambda n: '#{}'.format(n))
    buying = Decimal(random.random())
    selling = Decimal(random.uniform(0, float(buying)))


class GroupFactory(DjangoFactory):
    FACTORY_FOR = Group

    name = factory.Sequence(lambda n: 'Group {}'.format(n))
    completion_date = datetime.date.today() + datetime.timedelta(weeks=4)

    @factory.post_generation(extract_prefix='stocks')
    def create_contacts(self, create, extracted, **kwargs):
        # GroupFactory(stocks=[<stock1>, ...])
        if extracted:
            [StockGroupFactory(group=self, stock=contact) for contact in extracted]
        # GroupFactory(stocks__n=3)
        elif 'n' in kwargs:
            [StockGroupFactory(group=self, stock=RandomStockFactory()) for _ in range(int(kwargs['n']))]


class StockGroupFactory(DjangoFactory):
    FACTORY_FOR = StockGroup

    stock = factory.SubFactory(RandomStockFactory)
    group = factory.SubFactory(GroupFactory)
