"""

Template for Characters

Copy this module up one level and name it as you like, then
use it as a template to create your own Character class.

To make new logins default to creating characters
of your new type, change settings.BASE_CHARACTER_TYPECLASS to point to
your new class, e.g.

settings.BASE_CHARACTER_TYPECLASS = "game.gamesrc.objects.mychar.MyChar"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
import time
from ev import Character
from collections import OrderedDict
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from game.gamesrc.oasis.lib.oasis import action_watchers, check_ignores, check_sleepers, check_hiding, ignored_notifications
from game.gamesrc.oasis.lib.constants import ALERT
from object import WOObject

from lib.mail import get_messages
from web.character.models import TagCategory, TagDef, Tag
from settings import SERVERNAME

# these are called so many times it's worth setting them to avoid lookup calls
_GA = object.__getattribute__
_SA = object.__setattr__
_DA = object.__delattr__

User = get_user_model()

class WOCharacter(Character, WOObject):
    """
    The Character is like any normal Object (see example/object.py for
    a list of properties and methods), except it actually implements
    some of its hook methods to do some work:

    at_basetype_setup - always assigns the default_cmdset to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_disconnect - stores the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_post_login - retrieves the character's old location and puts it back
                    on the grid with a "charname has connected" message echoed
                    to the room

    """
    DELAY = 10
    def __str__(self):
        return self.name
    __repr__ = __str__

    def new_character(self):
        """
        Things to do when first setting up a character, even before connection.
        """
        self.db.stats = { 'Body': 0, 'Soul': 0, 'Mind': 0, 'Expression': 0, 'Focus': 0 }

    def announce_message(self, user, target, message, message_key, must_be_online=False):
        """
            Sends an announcement to other characters.
        message is a string to send.
        message_key is a label for the type of message being sent. An
            announcement that a user is connection might have this as "connection".
        must_be_online makes the message cancel if the user disconnects before
            the targets receive it.
        """
        if (must_be_online and not self.sessions) or (not check_hiding(user, [target])) or (not check_ignores(target, [self], silent=True) ) \
            or self.db.hiding or message_key in ignored_notifications(target):
            return
        target.msg(message)

    def get_tags(self, flat=False):
        """
            Get tags on this characted back, organized into an OrderedDict by
        category name. The tags in each category will also be a dictionary of
        true/false values. This method is only really practical if the number
        of defined tags remains relativly small.

        I'd say avoid doing this if you have more than a couple hundred tags.
        """
        tags_dict = {}
        categories = list(TagCategory.objects.all())
        tag_defs = list(TagDef.objects.all())
        character_tags = [tag.tag for tag in Tag.objects.filter(player=self.player) ]
        if flat:
            return character_tags
        for category in categories:
            tags_dict[category] = OrderedDict(sorted({tagdef : (tagdef in character_tags) for tagdef in TagDef.objects.filter(category=category)}.items(), key=lambda tagkey: tagkey[0].name))
        return tags_dict

    def get_alts(self, raw=False):
        """
            Get all verified alts of a character. If raw is true, gets even
        unverified characters. Don't use raw for security purpose, only for
        investigative purposes.
            If raw is false and the user is not active, always returns an empty
        list.
        """
        user = self.db.spirit
        if not raw and not user.is_active:
            return []
        try:
            alts = [alt.db.avatar for alt in User.objects.filter(email__iexact=user.email) if alt.is_active or raw]
            return alts
        except AttributeError:
            return []

    def check_list(self, target, listname, ignores=True):
        """
        Checks to see if target is in one of the character's personal lists.
        """
        list_to_check = getattr(self.db, listname)
        if not list_to_check:
            return False
        if target in list_to_check:
            if ignores:
                if not check_ignores(target, [self], silent=True):
                    return False
            return True
        return False

    def toggle_list(self, target, toggle, listname):
        """
        Toggles the presence of a user in a personal list.
        """
        CHARACTER = 0
        if toggle:
             character_list = getattr(self.db, listname)
             if not character_list:
                 character_list = []
             character_list.append(target)
             setattr(self.db, listname, character_list)
        else:
             old_list = getattr(self.db, listname)
             if not old_list:
                 old_list = []
             new_list = [ obj for obj in old_list if obj != target ]
             setattr(self.db, listname, new_list)


    def get_absolute_url(self):
        """
        Get the URL to a user's profile.
        """
        return reverse('character:profile', args=[self.name])

    def delete(self):
        """
        Delete the object with all standard checks, and any extras we've defined for it.
        """
        result = super(WOCharacter, self).delete()
        if result:
            for tag in Tag.objects.filter(character=self.dbobj):
                tag.delete()
        return result

    def at_post_puppet(self):
        """
        This recovers the character again after having been "stowed away" at disconnect.
        """
        if self.db.prelogout_location:
            # try to recover
            self.location = self.db.prelogout_location
        if self.location == None:
            # make sure location is never None (home should always exist)
            self.location = self.home
        # save location again to be sure
        self.db.prelogout_location = self.location

        if self.location:
            self.location.msg_contents("{c%s has connected." % self.name, exclude=[self])
            self.location.at_object_receive(self, self.location)
        # Save login time.
        if len(self.sessions) <= 1:
            self.db.laston = time.time()
        # Announce connection to watchers
        if len(self.sessions) == 1:
            message = ALERT % "Somewhere on %s, %s has connected." % ( SERVERNAME, self.name )
        else:
            message = ALERT % "Somewhere on %s, %s has reconnected." % ( SERVERNAME, self.name )
        action_watchers(self, self.announce_message, delay=WOCharacter.DELAY, kwargs={ 'message' : message, 'message_key' : 'connection', 'must_be_online' : True })
        print "I ran!"
        self.execute_cmd('look')
        self.execute_cmd('mail/check quiet')
        self.execute_cmd('watch')

    def at_after_move(self, source_location):
        if self.location and self.location.db.ic:
            self.db.ic_location = self.location
        super(WOCharacter, self).at_after_move(source_location)

    def unread_messages(character):
        READ = 2
        mail = get_messages(character)
        return [message for message in mail if not message[READ]]

    def at_pre_unpuppet(self):
        """
        We stow away the character when logging off, otherwise the character object will
        remain in the room also after the player logged off ("headless", so to speak).
        """
        if self.location: # have to check, in case of multiple connections closing
            if len(self.sessions) > 1:
                self.location.msg_contents("{c%s has dropped a connection.{n" % self.name, exclude=[self])
            else:
                self.location.msg_contents("{c%s has disconnected.{n" % self.name, exclude=[self])
                self.db.prelogout_location = self.location
                self.location = None
                self.db.lastoff = time.time()
                if not self.db.laston:
                    self.db.laston = 0
                if self.db.lastoff - self.db.laston >= WOCharacter.DELAY:
                    message = ALERT % "Somewhere on %s, %s has disconnected." % ( SERVERNAME, self.name )
                    action_watchers(self, self.announce_message, kwargs={ 'message' : message, 'message_key' : 'connection' })
