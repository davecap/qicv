# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AccountVerification'
        db.create_table('userprofiles_accountverification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('userprofiles', ['AccountVerification'])

        # Adding model 'EmailVerification'
        db.create_table('userprofiles_emailverification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('old_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('new_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('token', self.gf('django.db.models.fields.CharField')(default='b8c1a7f9-1f0b-4796-86de-c6efa3da170b', max_length=40)),
            ('code', self.gf('django.db.models.fields.CharField')(default='1a34bf94-1ca9-4ea7-b8b5-1bbeb98313db', max_length=40)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_expired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expiration_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 2, 27, 11, 47, 25, 140220))),
        ))
        db.send_create_signal('userprofiles', ['EmailVerification'])


    def backwards(self, orm):
        
        # Deleting model 'AccountVerification'
        db.delete_table('userprofiles_accountverification')

        # Deleting model 'EmailVerification'
        db.delete_table('userprofiles_emailverification')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'userprofiles.accountverification': {
            'Meta': {'object_name': 'AccountVerification'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'userprofiles.emailverification': {
            'Meta': {'object_name': 'EmailVerification'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'2cb9ccea-d030-4cec-83ab-738f3050f04b'", 'max_length': '40'}),
            'expiration_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 27, 11, 47, 25, 145289)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'old_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'b736a3b4-b97c-438d-83e0-58bdb0196131'", 'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['userprofiles']
