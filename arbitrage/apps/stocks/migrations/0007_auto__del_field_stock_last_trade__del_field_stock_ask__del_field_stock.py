# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Stock.last_trade'
        db.delete_column('stocks_stock', 'last_trade')

        # Deleting field 'Stock.ask'
        db.delete_column('stocks_stock', 'ask')

        # Deleting field 'Stock.bid'
        db.delete_column('stocks_stock', 'bid')

        # Adding field 'Stock.buying'
        db.add_column('stocks_stock', 'buying',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'Stock.selling'
        db.add_column('stocks_stock', 'selling',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=3, blank=True),
                      keep_default=False)

        # Deleting field 'Group.apr'
        db.delete_column('stocks_group', 'apr')

        # Deleting field 'Group.greatest_difference'
        db.delete_column('stocks_group', 'greatest_difference')

        # Deleting field 'StockGroup.lowest'
        db.delete_column('stocks_stockgroup', 'lowest')

        # Deleting field 'StockGroup.highest'
        db.delete_column('stocks_stockgroup', 'highest')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Stock.last_trade'
        raise RuntimeError("Cannot reverse this migration. 'Stock.last_trade' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Stock.ask'
        raise RuntimeError("Cannot reverse this migration. 'Stock.ask' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Stock.bid'
        raise RuntimeError("Cannot reverse this migration. 'Stock.bid' and its values cannot be restored.")
        # Deleting field 'Stock.buying'
        db.delete_column('stocks_stock', 'buying')

        # Deleting field 'Stock.selling'
        db.delete_column('stocks_stock', 'selling')


        # User chose to not deal with backwards NULL issues for 'Group.apr'
        raise RuntimeError("Cannot reverse this migration. 'Group.apr' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Group.greatest_difference'
        raise RuntimeError("Cannot reverse this migration. 'Group.greatest_difference' and its values cannot be restored.")
        # Adding field 'StockGroup.lowest'
        db.add_column('stocks_stockgroup', 'lowest',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'StockGroup.highest'
        db.add_column('stocks_stockgroup', 'highest',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'stocks.group': {
            'Meta': {'object_name': 'Group'},
            'completion_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stocks.Stock']", 'through': "orm['stocks.StockGroup']", 'symmetrical': 'False'})
        },
        'stocks.stock': {
            'Meta': {'object_name': 'Stock'},
            'buying': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '3', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrade_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'selling': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '3', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'symbol': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'stocks.stockgroup': {
            'Meta': {'object_name': 'StockGroup'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stockgroups'", 'to': "orm['stocks.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_side': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stockgroup'", 'unique': 'True', 'to': "orm['stocks.Stock']"})
        }
    }

    complete_apps = ['stocks']