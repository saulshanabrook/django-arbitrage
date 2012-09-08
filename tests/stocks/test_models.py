from decimal import Decimal

from django.test import TestCase

from arbitrage.apps.stocks import api
from . import factories


class StockTestCase(TestCase):
    def test_intrade_save(self):
        stock = factories.ObamaStockIntradeFactory()
        stock.sync()


class ApiTestCase(TestCase):
    def test_intrade_fields_limited(self):
        """
        Tests that ``get_intrade_fields`` returns only the fields specifed
        """
        fields = ['bid', 'offer']
        returned = api.get_intrade_fields(743474, fields)
        # returned dict has same keys as input fields of items
        self.assertItemsEqual(returned.keys(), fields)

    def test_intrade_returns_decimal(self):
        """
        Tests that ``get_intrade_fields`` returns a appropriate Decimal values
        for decimal fields
        """
        decimal_fields = ['bid', 'offer']
        returned = api.get_intrade_fields(743474, fields=decimal_fields)
        for decimal_value in returned.values():
            self.assertIsInstance(decimal_value, Decimal)
            self.assertLessEqual(decimal_value, 1)
            self.assertGreaterEqual(decimal_value, 0)


class GroupTestCase(TestCase):
    def test_greatest_difference(self):
        group = factories.GroupFactory()
        factories.StockGroupFactory(stock__buying=Decimal(.85),
                                    stock__selling=Decimal(.8),
                                    group=group)
        factories.StockGroupFactory(stock__buying=Decimal(.4),
                                    stock__selling=Decimal(.35),
                                    other_side=True,
                                    group=group)
        self.assertEqual(group.highest_buy.buying, Decimal('.85'))
        self.assertEqual(group.lowest_sell.selling, Decimal('.6'))
        self.assertEqual(group.greatest_difference, Decimal('.25'))
