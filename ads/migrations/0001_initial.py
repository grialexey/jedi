# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ad'
        db.create_table('ads_ad', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='other', max_length=10)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('added', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ads.Author'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('ads', ['Ad'])

        # Adding model 'Author'
        db.create_table('ads_author', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ads', ['Author'])


    def backwards(self, orm):
        # Deleting model 'Ad'
        db.delete_table('ads_ad')

        # Deleting model 'Author'
        db.delete_table('ads_author')


    models = {
        'ads.ad': {
            'Meta': {'ordering': "['-added']", 'object_name': 'Ad'},
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ads.Author']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'ads.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ads']