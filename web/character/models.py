from datetime import datetime
from django.db import models
from src.objects.models import ObjectDB
from src.players.models import PlayerDB

class TagCategory(models.Model):
    """
    Categories of Role-Play Preferences
    """
    name = models.CharField(max_length=30, unique=True)
    def __unicode__(self):
        return unicode(self.name)

class TagDef(models.Model):
    """
    Tags used for Role-Play Preferences.
    """
    name = models.CharField(max_length=30)
    category = models.ForeignKey(TagCategory, db_index=True, related_name='+')
    description = models.TextField()
    def __unicode__(self):
        return unicode(self.name)
    def character_check(self, character):
        """
            Check to see if a character has this tag.
        """
        if Tag.objects.filter(tag=self, character=character):
            return True
        else:
            return False

class Tag(models.Model):
    """
    The actual tags stored.
    """
    def __unicode__(self):
        try:
            return unicode(self.tag.name)
        except:
            return unicode("((Defunct))")
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    tag = models.ForeignKey(TagDef, db_index=True)

class PlayerSortName(models.Model):
    """
    Categorical definitions of player list types.
    """
    name = models.CharField(max_length=30, unique=True)
    def __unicode__(self):
        return unicode(self.name)

class PlayerSort(models.Model):
    """
    A list of players one may keep to define things like friends lists, or ignores.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    target = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    category = models.ForeignKey(PlayerSortName, db_index=True, related_name='+')

class StaffNote(models.Model):
    """
    Notes written by staff members about a player and their application.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    staffer = models.ForeignKey(ObjectDB, db_index=True, null=True, default=None, related_name='+')
    time = models.DateTimeField(auto_now_add=True)

class StatDef(models.Model):
    """
    Class used for defining the stats the game uses.
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=4086)

class Stat(models.Model):
    """
    The value of a stat for a character.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    category = models.ForeignKey(StatDef, related_name='+')
    value = models.IntegerField(default=0)

class Quality(models.Model):
    """
    Custom Character Qualities.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=280)

class Approval(models.Model):
    """
    Approval Status.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, unique=True)
    time_submitted = models.DateTimeField(default=datetime.now, db_index=True)
    approvers = models.ManyToManyField(ObjectDB, related_name='+', default=None, symmetrical=False)
    queued = models.BooleanField(default=True)

class CharacterInfo(models.Model):
    """
    Character's Description and Background.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, unique=True, related_name='+')
    background = models.TextField(max_length=32768)
    upgrades = models.IntegerField(default=0)

class ApplaudCategory(models.Model):
    """
    A category of applause for a user.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    name = models.CharField(max_length=30)
    archived = models.BooleanField(default=False)

class Applaud(models.Model):
    """
    A commendation given from one user to another.
    """
    character = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    applauder = models.ForeignKey(ObjectDB, db_index=True, related_name='+')
    category = models.ForeignKey(ApplaudCategory, db_index=True, related_name='+')
    time = models.DateField(auto_now_add=True)
    scene_desc = models.TextField(max_length=2048)
    action_desc = models.TextField(max_length=2048)
