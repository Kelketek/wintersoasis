from haystack import site
from haystack.indexes import SearchIndex, CharField
from src.objects.models import ObjectDB

class CharacterIndex(SearchIndex):
    text = CharField(document=True)
    name = CharField()
    species = CharField()
    def prepare_text(self, thing):
        if thing.dbobj.db.desc:
            return thing.dbobj.db.desc
    def prepare_species(self, thing):
        if thing.dbobj.db.species:
            return thing.dbobj.db.species

site.register(ObjectDB, CharacterIndex)
