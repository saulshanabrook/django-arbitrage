# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.name'
        db.add_column('stocks_group', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Name', unique=True, max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Group.name'
        db.delete_column('stocks_group', 'name')


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
            'highest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lowest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'side_one': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stocks.Stock']", 'unique': 'True'})
        }
    }

    complete_apps = ['stocks']