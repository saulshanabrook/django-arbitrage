# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'StockGroupRelationship'
        db.delete_table('stocks_stockgrouprelationship')

        # Adding model 'Group'
        db.create_table('stocks_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('completion_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('stocks', ['Group'])

        # Deleting field 'StockGroup.completion_date'
        db.delete_column('stocks_stockgroup', 'completion_date')

        # Adding field 'StockGroup.stock'
        db.add_column('stocks_stockgroup', 'stock',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['stocks.Stock'], unique=True),
                      keep_default=False)

        # Adding field 'StockGroup.group'
        db.add_column('stocks_stockgroup', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['stocks.Group']),
                      keep_default=False)

        # Adding field 'StockGroup.side_one'
        db.add_column('stocks_stockgroup', 'side_one',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'StockGroup.lowest'
        db.add_column('stocks_stockgroup', 'lowest',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'StockGroup.highest'
        db.add_column('stocks_stockgroup', 'highest',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'StockGroupRelationship'
        db.create_table('stocks_stockgrouprelationship', (
            ('side_one', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stocks.StockGroup'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stocks.Stock'], unique=True)),
        ))
        db.send_create_signal('stocks', ['StockGroupRelationship'])

        # Deleting model 'Group'
        db.delete_table('stocks_group')


        # User chose to not deal with backwards NULL issues for 'StockGroup.completion_date'
        raise RuntimeError("Cannot reverse this migration. 'StockGroup.completion_date' and its values cannot be restored.")
        # Deleting field 'StockGroup.stock'
        db.delete_column('stocks_stockgroup', 'stock_id')

        # Deleting field 'StockGroup.group'
        db.delete_column('stocks_stockgroup', 'group_id')

        # Deleting field 'StockGroup.side_one'
        db.delete_column('stocks_stockgroup', 'side_one')

        # Deleting field 'StockGroup.lowest'
        db.delete_column('stocks_stockgroup', 'lowest')

        # Deleting field 'StockGroup.highest'
        db.delete_column('stocks_stockgroup', 'highest')


    models = {
        'stocks.group': {
            'Meta': {'object_name': 'Group'},
            'completion_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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