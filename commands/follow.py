"""
    Follow. Allows for checking when a user you follow is online and if they
post status updates.
"""

from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from game.gamesrc.oasis.lib.constants import ALERT
from game.gamesrc.oasis.lib.oasis import validate_targets, toggle_notifications, object_stamp, current_object, check_ignores, check_sleepers, check_hiding, distill_list, ferment_list

class Follow(default_cmds.MuxCommand):
    """
    Get alerted if someone you follow connects or is doing something new!

    If you want to follow someone named Thaddius:
        follow Thaddius
    If you want to stop getting updates on Thaddius:
        unfollow Thaddius
    If you want to see which of the people you are following and if they're online:
        follow
    To disable online/offline notifications, do:
        follow/noconnects
    ...And to turn them back on, do:
        follow/connects
    To disable status updates, do:
        follow/nostatus
    ...And to resubscribe, do:
        follow/status
    To get a list of everyone you're following:
        follow/list
    """
    key = "Follow"
    aliases = ["wf", "watchfor", "friend"]
    locks = "cmd:all()"
    help_category = "General"
    follow = True
    success_verbage = "Now following"
    redundant_verbage = "You are already following"

    def display_following(self):
        following_list = distill_list(self.caller.db.following)
        if not following_list:
            self.caller.msg(ALERT % "You are not following anyone. If you find someone interesting, or meet a friend, be sure to follow them with: follow YourFriend'sNameHere")
            return
        following_list = check_ignores(self.caller, following_list, silent=True)
        following_list = check_sleepers(self.caller, following_list, silent=True)
        following_list = check_hiding(self.caller, following_list)
        ROW_LENGTH = 4
        following_list = [following_list[i:i+ROW_LENGTH] for i in range(0, len(following_list), ROW_LENGTH)]
        if not following_list:
            self.caller.msg("{cNo one you are following is online.{n")
            return
        self.caller.msg("{cPeople online that you are following:{n")
        for group in following_list:
            self.caller.msg("%-20s"*len(group) % tuple(group))

    def remove_from_list(self, propname, success, redundant):
        """
            Add a user to a list, letting them know if the work is redundant.
        If announce_online is true, lets the user know if the target is
        currently online.
        """
        object_list = distill_list(getattr(self.caller.db, propname))
        removing_list = validate_targets(self.caller, self.arglist, ignores=False, local_only=False)
        net_list = []
        for item in removing_list:
            if item not in object_list:
                self.caller.msg(ALERT % "%s %s." % (redundant, item.name))
            else:
                net_list.append(item)
        for item in net_list:
            self.caller.msg(ALERT % "%s %s." % (success, item.name))
        cleaned_list = [ item for item in object_list if item not in net_list ]
        setattr(self.caller.db, propname, ferment_list(cleaned_list))

    def add_to_list(self, propname, success, redundant, announce_online=False):
        """
            Add a user to a list, letting them know if the work is redundant.
        If announce_online is true, lets the user know if the target is
        currently online.
        """
        object_list = distill_list(getattr(self.caller.db, propname))
        adding_list = validate_targets(self.caller, self.arglist, ignores=False, local_only=False)
        net_list = []
        for item in adding_list:
            if item in object_list:
                self.caller.msg(ALERT % "%s %s." % (redundant, item.name))
            else:
                net_list.append(item)
        for item in net_list:
            if announce_online and item.sessions and check_ignores(self.caller, [item], silent=True) and check_hiding(self.caller, [item]):
                self.caller.msg(ALERT % "%s is currently online." % item.name)
            self.caller.msg(ALERT % "%s %s." % (success, item.name))
        setattr(self.caller.db, propname, ferment_list(object_list + net_list))

    def func(self):
        """
        Main routing function.
        """
        self.switches = [ switch.lower() for switch in self.switches ]
        if not self.switches:
            if self.args:
                if self.follow:
                    self.add_to_list('following', self.success_verbage, self.redundant_verbage)
                else:
                    self.remove_from_list('following', self.success_verbage, self.redundant_verbage)
            else:
                self.display_following()
        elif 'noconnects' in self.switches:
            toggle_notifications(self.caller, 'connection', False)
            self.caller.msg(ALERT % "You will not receive further connection alerts.")
        elif 'connects' in self.switches:
            toggle_notifications(self.caller, 'connection', True)
            self.caller.msg(ALERT % "You are now tuned in to connection alerts for those you are following.")
        elif 'nostatus' in self.switches:
            toggle_notifications(self.caller, 'status', False)
            self.caller.msg(ALERT % "No longer receiving status messages.")
        elif 'status' in self.switches:
            toggle_notifications(self.caller, 'status', True)
            self.caller.msg(ALERT % "You are now tuned in to status updates from those you are following.")
        elif 'list' in self.switches:
            self.caller.msg(', '.join([ character.name for character in distill_list(self.caller.db.following)]))

class Unfollow(Follow):
    """
    Stop being such a creeper.

    To stop following Thaddius:
        unfollow Thaddius
    """
    key = "Unfollow"
    aliases = ["unfriend"]  
    locks = "cmd:all()"
    help_category = "General"
    follow = False
    success_verbage = "Unfollowing"
    redundant_verbage = "You weren't following"
