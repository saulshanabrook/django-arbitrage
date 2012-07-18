# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.greatest_difference'
        db.add_column('stocks_group', 'greatest_difference',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=3, decimal_places=3),
                      keep_default=False)

        # Adding field 'Group.apr'
        db.add_column('stocks_group', 'apr',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=5),
                      keep_default=False)

        # Deleting field 'StockGroup.lowest'
        db.delete_column('stocks_stockgroup', 'lowest')

        # Deleting field 'StockGroup.highest'
        db.delete_column('stocks_stockgroup', 'highest')


    def backwards(self, orm):
        # Deleting field 'Group.greatest_difference'
        db.delete_column('stocks_group', 'greatest_difference')

        # Deleting field 'Group.apr'
        db.delete_column('stocks_group', 'apr')

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
            'apr': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '5'}),
            'completion_date': ('django.db.models.fields.DateField', [], {}),
            'greatest_difference': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stocks.Stock']", 'through': "orm['stocks.StockGroup']", 'symmetrical': 'False'})
        },
        'stocks.stock': {
            'Meta': {'object_name': 'Stock'},
            'ask': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'bid': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrade_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_trade': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'symbol': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'stocks.stockgroup': {
            'Meta': {'object_name': 'StockGroup'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stocks.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side_one': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stocks.Stock']", 'unique': 'True'})
        }
    }

    complete_apps = ['stocks']