from haystack import site
from haystack.indexes import SearchIndex, CharField
from src.players.models import PlayerDB

class CharacterIndex(SearchIndex):
    text = CharField(document=True)
    name = CharField(boost=1.5)
    species = CharField()
    background = CharField(boost=1.25)
    qualities = CharField(boost=1.10)
    tags = CharField(boost=1.5)
    def prepare_text(self, thing):
        if thing.character.db.desc:
            return thing.character.db.desc
    def prepare_species(self, thing):
        if thing.character.db.species:
            return thing.character.db.species
    def prepare_qualities(self, thing):
        if thing.character.db.qualities:
            return str(thing.character.db.qualities)
    def prepare_background(self, thing):
        if thing.character.db.background:
            return str(thing.character.db.background)
    def prepare_tags(self, thing):
        return str(thing.character.get_tags())
        

site.register(PlayerDB, CharacterIndex)
