# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stock'
        db.create_table('stocks_stock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('intrade_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('last_trade', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=3)),
            ('bid', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=3)),
            ('ask', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=3)),
        ))
        db.send_create_signal('stocks', ['Stock'])

        # Adding model 'StockGroup'
        db.create_table('stocks_stockgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('completion_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('stocks', ['StockGroup'])

        # Adding model 'StockGroupRelationship'
        db.create_table('stocks_stockgrouprelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stocks.Stock'], unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stocks.StockGroup'])),
            ('side_one', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stocks', ['StockGroupRelationship'])


    def backwards(self, orm):
        # Deleting model 'Stock'
        db.delete_table('stocks_stock')

        # Deleting model 'StockGroup'
        db.delete_table('stocks_stockgroup')

        # Deleting model 'StockGroupRelationship'
        db.delete_table('stocks_stockgrouprelationship')


    models = {
        'stocks.stock': {
            'Meta': {'object_name': 'Stock'},
            'ask': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'bid': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrade_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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