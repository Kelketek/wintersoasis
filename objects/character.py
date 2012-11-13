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
from game.gamesrc.oasis.lib.oasis import action_followers, current_object, check_ignores, check_sleepers, check_hiding, ignored_notifications
from game.gamesrc.oasis.lib.constants import ALERT
from settings import SERVERNAME

class WOCharacter(Character):
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

    def at_post_login(self):
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

        self.location.msg_contents("{c%s has connected." % self.name, exclude=[self])
        self.location.at_object_receive(self, self.location)
        # Save login time.
        if len(self.sessions) <= 1:
            self.db.laston = time.time()
        # Announce connection to followers
        if len(self.sessions) == 1:
            message = ALERT % "Somewhere on %s, %s has connected." % ( SERVERNAME, self.name )
        else:
            message = ALERT % "Somewhere on %s, %s has reconnected." % ( SERVERNAME, self.name )
        action_followers(self, self.announce_message, delay=WOCharacter.DELAY, kwargs={ 'message' : message, 'message_key' : 'connection', 'must_be_online' : True })
        # Call look.
        self.execute_cmd('look')
        self.execute_cmd('mail/check quiet')
        self.execute_cmd('follow')

    def at_disconnect(self):
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
                if self.db.lastoff - self.db.laston >= WOCharacter.DELAY:
                    message = ALERT % "Somewhere on %s, %s has disconnected." % ( SERVERNAME, self.name )
                    action_followers(self, self.announce_message, kwargs={ 'message' : message, 'message_key' : 'connection' })
