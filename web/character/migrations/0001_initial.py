# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagCategory'
        db.create_table('character_tagcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('character', ['TagCategory'])

        # Adding model 'TagDef'
        db.create_table('character_tagdef', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['character.TagCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('character', ['TagDef'])

        # Adding model 'Tag'
        db.create_table('character_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character.TagDef'])),
        ))
        db.send_create_signal('character', ['Tag'])

        # Adding model 'PlayerSortName'
        db.create_table('character_playersortname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('character', ['PlayerSortName'])

        # Adding model 'PlayerSort'
        db.create_table('character_playersort', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['character.PlayerSortName'])),
        ))
        db.send_create_signal('character', ['PlayerSort'])

        # Adding model 'StaffNote'
        db.create_table('character_staffnote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('staffer', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', null=True, to=orm['players.PlayerDB'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('character', ['StaffNote'])

        # Adding model 'StatDef'
        db.create_table('character_statdef', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4086)),
        ))
        db.send_create_signal('character', ['StatDef'])

        # Adding model 'Stat'
        db.create_table('character_stat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['character.StatDef'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('character', ['Stat'])

        # Adding model 'Quality'
        db.create_table('character_quality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=280)),
        ))
        db.send_create_signal('character', ['Quality'])

        # Adding model 'Approval'
        db.create_table('character_approval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.PlayerDB'], unique=True)),
            ('time_submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('queued', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('character', ['Approval'])

        # Adding M2M table for field approvers on 'Approval'
        db.create_table('character_approval_approvers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('approval', models.ForeignKey(orm['character.approval'], null=False)),
            ('playerdb', models.ForeignKey(orm['players.playerdb'], null=False))
        ))
        db.create_unique('character_approval_approvers', ['approval_id', 'playerdb_id'])

        # Adding model 'CharacterInfo'
        db.create_table('character_characterinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', unique=True, to=orm['players.PlayerDB'])),
            ('background', self.gf('django.db.models.fields.TextField')(max_length=32768)),
            ('upgrades', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('character', ['CharacterInfo'])

        # Adding model 'ApplaudCategory'
        db.create_table('character_applaudcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('character', ['ApplaudCategory'])

        # Adding model 'Applaud'
        db.create_table('character_applaud', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('applauder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['players.PlayerDB'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['character.ApplaudCategory'])),
            ('time', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('scene_desc', self.gf('django.db.models.fields.TextField')(max_length=2048)),
            ('action_desc', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal('character', ['Applaud'])


    def backwards(self, orm):
        # Deleting model 'TagCategory'
        db.delete_table('character_tagcategory')

        # Deleting model 'TagDef'
        db.delete_table('character_tagdef')

        # Deleting model 'Tag'
        db.delete_table('character_tag')

        # Deleting model 'PlayerSortName'
        db.delete_table('character_playersortname')

        # Deleting model 'PlayerSort'
        db.delete_table('character_playersort')

        # Deleting model 'StaffNote'
        db.delete_table('character_staffnote')

        # Deleting model 'StatDef'
        db.delete_table('character_statdef')

        # Deleting model 'Stat'
        db.delete_table('character_stat')

        # Deleting model 'Quality'
        db.delete_table('character_quality')

        # Deleting model 'Approval'
        db.delete_table('character_approval')

        # Removing M2M table for field approvers on 'Approval'
        db.delete_table('character_approval_approvers')

        # Deleting model 'CharacterInfo'
        db.delete_table('character_characterinfo')

        # Deleting model 'ApplaudCategory'
        db.delete_table('character_applaudcategory')

        # Deleting model 'Applaud'
        db.delete_table('character_applaud')


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
            'applauder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.ApplaudCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
            'scene_desc': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'time': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'character.applaudcategory': {
            'Meta': {'object_name': 'ApplaudCategory'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"})
        },
        'character.approval': {
            'Meta': {'object_name': 'Approval'},
            'approvers': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['players.PlayerDB']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.PlayerDB']", 'unique': 'True'}),
            'queued': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'})
        },
        'character.characterinfo': {
            'Meta': {'object_name': 'CharacterInfo'},
            'background': ('django.db.models.fields.TextField', [], {'max_length': '32768'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['players.PlayerDB']"}),
            'upgrades': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'character.playersort': {
            'Meta': {'object_name': 'PlayerSort'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.PlayerSortName']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"})
        },
        'character.playersortname': {
            'Meta': {'object_name': 'PlayerSortName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'character.quality': {
            'Meta': {'object_name': 'Quality'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '280'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"})
        },
        'character.staffnote': {
            'Meta': {'object_name': 'StaffNote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
            'staffer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': "orm['players.PlayerDB']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'character.stat': {
            'Meta': {'object_name': 'Stat'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['character.StatDef']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['players.PlayerDB']"}),
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