from django.db import models
from src.objects.models import ObjectDB

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
    category = models.ForeignKey(TagCategory, db_index=True)
    description = models.TextField()
    def __unicode__(self):
        return unicode(self.name)

class Tag(models.Model):
    """
    The actual tags stored.
    """
    def __unicode__(self):
        try:
            return unicode(self.tag.name)
        except:
            return unicode("((Defunct))")
    character = models.ForeignKey(ObjectDB, db_index=True)
    tag = models.ForeignKey(TagDef, db_index=True)
