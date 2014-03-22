# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'APNTokenModel'
        db.create_table(u'apn_apntokenmodel', (
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
        ))
        db.send_create_signal(u'apn', ['APNTokenModel'])


    def backwards(self, orm):
        # Deleting model 'APNTokenModel'
        db.delete_table(u'apn_apntokenmodel')


    models = {
        u'apn.apntokenmodel': {
            'Meta': {'object_name': 'APNTokenModel'},
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['apn']