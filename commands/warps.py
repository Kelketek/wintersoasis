"""
Warp commands. takes a user to special places on the MUCK, saving state as needed.
"""
import time
from game.gamesrc.oasis.lib.constants import *
import ev
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from src.server.sessionhandler import SESSIONS
from settings import *
from lib.oasis import current_object

MAIN = 0

def pre_warp(caller):
    """
    Thing to do before warping someone.
    """
    message = "{y>> {C%s is loaded into a giant steam cannon and PUM!ed away.{n" % caller
    caller.location.at_say(caller, message)
    caller.location.msg_contents(message)

def post_warp(caller):
    """
    Thing to do after warping someone.
    """
    message = "{y>> {C%s crash-lands into the ground with a considerable THUD!{n" % caller
    caller.location.at_say(caller, message)
    caller.location.msg_contents(message)


class Nexus(default_cmds.MuxCommand):
    """
        Warp to the OOC Nexus.
    """
    # these need to be specified

    key = "nexus"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        nexus = ev.search_object(NEXUS)[MAIN]
        if self.caller.location == nexus:
            self.caller.msg("{rYou are already in the Nexus.{n")
            return
        if self.caller.location and self.caller.location.db.ic:
            self.caller.msg("\n{gYour location has been saved.{n\n")
        pre_warp(self.caller)
        self.caller.move_to(nexus,quiet=True)
        post_warp(self.caller)

class IC(default_cmds.MuxCommand):
    """
         Warp back to the IC realm.
    """
    key = "ic"
    locks = "cmd:semi_approved()"

    def func(self):
        default_location = ev.search_object(IC_START)[MAIN]
        last_location = self.caller.db.ic_location
        if last_location:
            last_location = current_object(last_location)
        else:
            last_location = default_location
        self.switches = [switch.lower() for switch in self.switches]
        if self.caller.location and self.caller.location.db.ic and 'reset' not in self.switches:
            self.caller.msg("{rYou are already in an IC area!{n")
            return
        if 'reset' in self.switches:
            del self.caller.db.ic_location
            if self.caller.location and self.caller.location.db.ic:     
                self.caller.msg("\n{yYour IC location has been reset the starting point.{n\n")
            last_location = default_location
        pre_warp(self.caller)
        self.caller.move_to(last_location)
        post_warp(self.caller)
        if not last_location == default_location:
            self.caller.msg("{y>> {CYou have been returned to your last saved IC location. If there is an error with this warp, or if you are lost, type {gIC/reset{n")
        else:
            self.caller.msg("{y>> {CYou are at the IC realm starting point. To return to the OOC realm, type {gnexus{C.{n")
