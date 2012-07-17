import factory

from arbitrage.apps.stocks.models import Stock


class StockIntradeFactory(factory.Factory):
    FACTORY_FOR = Stock

    site = 'intrade'
    intrade_id = 743474
