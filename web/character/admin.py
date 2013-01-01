from django.contrib import admin
from character.models import TagDef, TagCategory, Tag

admin.site.register(TagDef)
admin.site.register(TagCategory)
admin.site.register(Tag)
