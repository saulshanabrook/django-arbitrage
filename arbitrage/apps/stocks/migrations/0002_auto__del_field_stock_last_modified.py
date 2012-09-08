# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Stock.last_modified'
        db.delete_column('stocks_stock', 'last_modified')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Stock.last_modified'
        raise RuntimeError("Cannot reverse this migration. 'Stock.last_modified' and its values cannot be restored.")

    models = {
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
            'completion_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stocks.Stock']", 'through': "orm['stocks.StockGroupRelationship']", 'symmetrical': 'False'})
        },
        'stocks.stockgrouprelationship': {
            'Meta': {'object_name': 'StockGroupRelationship'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stocks.StockGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'side_one': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stocks.Stock']", 'unique': 'True'})
        }
    }

    complete_apps = ['stocks']