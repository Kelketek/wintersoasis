# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CharacterInfo.species'
        db.delete_column('character_characterinfo', 'species')


    def backwards(self, orm):
        # Adding field 'CharacterInfo.species'
        db.add_column('character_characterinfo', 'species',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)


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
        'character.applaud': {
            'Meta': {'object_name': 'Applaud'},
            'action_desc': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'applauder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.ApplaudCategory']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scene_desc': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'time': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'character.applaudcategory': {
            'Meta': {'object_name': 'ApplaudCategory'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'character.approval': {
            'Meta': {'object_name': 'Approval'},
            'approvers': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['objects.ObjectDB']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['objects.ObjectDB']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'queued': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'})
        },
        'character.characterinfo': {
            'Meta': {'object_name': 'CharacterInfo'},
            'background': ('django.db.models.fields.TextField', [], {'max_length': '32768'}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upgrades': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'character.playersort': {
            'Meta': {'object_name': 'PlayerSort'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.PlayerSortName']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"})
        },
        'character.playersortname': {
            'Meta': {'object_name': 'PlayerSortName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'character.quality': {
            'Meta': {'object_name': 'Quality'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '280'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'character.staffnote': {
            'Meta': {'object_name': 'StaffNote'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staffer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['objects.ObjectDB']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'character.stat': {
            'Meta': {'object_name': 'Stat'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.StatDef']"}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'character.statdef': {
            'Meta': {'object_name': 'StatDef'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4086'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'character.tag': {
            'Meta': {'object_name': 'Tag'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['objects.ObjectDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character.TagDef']"})
        },
        'character.tagcategory': {
            'Meta': {'object_name': 'TagCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'character.tagdef': {
            'Meta': {'object_name': 'TagDef'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.TagCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'objects.objectdb': {
            'Meta': {'object_name': 'ObjectDB'},
            'db_cmdset_storage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'db_date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'db_destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'destinations_set'", 'null': 'True', 'to': "orm['objects.ObjectDB']"}),
            'db_home': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'homes_set'", 'null': 'True', 'to': "orm['objects.ObjectDB']"}),
            'db_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'db_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations_set'", 'null': 'True', 'to': "orm['objects.ObjectDB']"}),
            'db_lock_storage': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'db_permissions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'db_player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.PlayerDB']", 'null': 'True', 'blank': 'True'}),
            'db_typeclass_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'players.playerdb': {
            'Meta': {'object_name': 'PlayerDB'},
            'db_cmdset_storage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'db_date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'db_is_connected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'db_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'db_lock_storage': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'db_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['objects.ObjectDB']", 'null': 'True', 'blank': 'True'}),
            'db_permissions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'db_typeclass_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['character']