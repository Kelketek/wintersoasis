from src.players.player import Player
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import get_template

# these are called so many times it's worth defining them to avoid lookup calls
_GA = object.__getattribute__
_SA = object.__setattr__
_DA = object.__delattr__

class WOPlayer(Player):

    def get_absolute_url(self):
        """
        Get the URL to a user's profile.
        """
        return reverse('character:profile', args=[self.name])

    def html_snippet(self):
        """
        A snippet of HTML rendered from a Django template.
        """
        template = get_template('search/character.html')
        return template.render(Context({'user':self.user, 'character':self.character}))

    def character(self):
        """
        Gets the primary character for this player.
        """
        return self.db.character
