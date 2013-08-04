"""
    Follow. Allows for checking when a user you watch is online and if they
post status updates.
"""

from ev import default_cmds
from game.gamesrc.oasis.lib.constants import ALERT
from game.gamesrc.oasis.lib.oasis import validate_targets, toggle_notifications, check_ignores, check_sleepers, check_hiding

class Watch(default_cmds.MuxCommand):
    """
    Get alerted if someone you watch connects or is doing something new!

    If you want to watch someone named Thaddius:
        watch Thaddius
    If you want to stop getting updates on Thaddius:
        watch Thaddius
    If you want to see which of the people you are watching and if they're online:
        watch
    To disable online/offline notifications, do:
        watch/noconnects
    ...And to turn them back on, do:
        watch/connects
    To disable status updates, do:
        watch/nostatus
    ...And to resubscribe, do:
        watch/status
    To get a list of everyone you're watching:
        watch/list
    """
    key = "Watch"
    aliases = ["wf", "watchfor", "friend"]
    locks = "cmd:all()"
    help_category = "General"
    watch = True
    success_verbage = "Now watching"
    redundant_verbage = "You are already watching"

    def display_watching(self):
        watching_list = self.caller.db.watching
        if not watching_list:
            self.caller.msg(ALERT % "You are not watching anyone. If you find someone interesting, or meet a friend, be sure to watch them with: watch {yYourFriend'sNameHere{n")
            return
        watching_list = check_ignores(self.caller, watching_list, silent=True)
        watching_list = check_sleepers(self.caller, watching_list, silent=True)
        watching_list = check_hiding(self.caller, watching_list)
        ROW_LENGTH = 4
        watching_list = [watching_list[i:i+ROW_LENGTH] for i in range(0, len(watching_list), ROW_LENGTH)]
        if not watching_list:
            self.caller.msg("{cNo one you are watching is online.{n")
            return
        self.caller.msg("{cPeople online that you are watching:{n")
        for group in watching_list:
            self.caller.msg("%-20s"*len(group) % tuple(group))

    def remove_from_list(self, propname, success, redundant):
        """
            Add a user to a list, letting them know if the work is redundant.
        If announce_online is true, lets the user know if the target is
        currently online.
        """
        object_list = getattr(self.caller.db, propname)
        if not object_list:
            object_list = []
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
        setattr(self.caller.db, propname, cleaned_list)

    def add_to_list(self, propname, success, redundant, announce_online=False):
        """
            Add a user to a list, letting them know if the work is redundant.
        If announce_online is true, lets the user know if the target is
        currently online.
        """
        object_list = getattr(self.caller.db, propname)
        if not object_list:
            object_list = []
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
            object_list.extend(net_list)
        setattr(self.caller.db, propname, object_list)

    def func(self):
        """
        Main routing function.
        """
        self.switches = [ switch.lower() for switch in self.switches ]
        if not self.switches:
            if self.args:
                if self.watch:
                    self.add_to_list('watching', self.success_verbage, self.redundant_verbage)
                else:
                    self.remove_from_list('watching', self.success_verbage, self.redundant_verbage)
            else:
                self.display_watching()
        elif 'noconnects' in self.switches:
            toggle_notifications(self.caller, 'connection', False)
            self.caller.msg(ALERT % "You will not receive further connection alerts.")
        elif 'connects' in self.switches:
            toggle_notifications(self.caller, 'connection', True)
            self.caller.msg(ALERT % "You are now tuned in to connection alerts for those you are watching.")
        elif 'nostatus' in self.switches:
            toggle_notifications(self.caller, 'status', False)
            self.caller.msg(ALERT % "No longer receiving status messages.")
        elif 'status' in self.switches:
            toggle_notifications(self.caller, 'status', True)
            self.caller.msg(ALERT % "You are now tuned in to status updates from those you are watching.")
        elif 'list' in self.switches:
            watching = self.caller.db.watching
            if not watching:
                self.caller.msg("{rYou aren't watching anyone.{n")
            self.caller.msg(', '.join([ character.name for character in watching]))

class Unwatch(Watch):
    """
    Stop being such a creeper.

    To stop watching Thaddius:
        unwatch Thaddius
    """
    key = "Unwatch"
    aliases = ["unfriend", 'unwf']  
    locks = "cmd:all()"
    help_category = "General"
    watch = False
    success_verbage = "Unwatching"
    redundant_verbage = "You weren't watching"
