# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleModel'
        db.create_table(u'synchronize_articlemodel', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('article', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('audio_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'synchronize', ['ArticleModel'])


    def backwards(self, orm):
        # Deleting model 'ArticleModel'
        db.delete_table(u'synchronize_articlemodel')


    models = {
        u'synchronize.articlemodel': {
            'Meta': {'object_name': 'ArticleModel'},
            'article': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'audio_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['synchronize']