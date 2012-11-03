"""
Page command. Used to contact another player across the MUCK.
"""

import time
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from src.server.sessionhandler import SESSIONS
from settings import *
from game.gamesrc.oasis.lib.oasis import partial_pmatch


"""
This sets up the basis for a Evennia's 'MUX-like' command
    style. The idea is that most other Mux-related commands should
    just inherit from this and don't have to implement parsing of
    their own unless they do something particularly advanced.

A MUXCommand command understands the following possible syntax:

    name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

The 'name[ with several words]' part is already dealt with by the
    cmdhandler at this point, and stored in self.cmdname. The rest is stored
    in self.args.

The MuxCommand parser breaks self.args into its constituents and stores them in the
    following variables:

self.switches = optional list of /switches (without the /)
self.raw = This is the raw argument input, including switches
self.args = This is re-defined to be everything *except* the switches
self.lhs = Everything to the left of = (lhs:'left-hand side'). If
    no = is found, this is identical to self.args.
self.rhs: Everything to the right of = (rhs:'right-hand side').
    If no '=' is found, this is None.
self.lhslist - self.lhs split into a list by comma
self.rhslist - list of self.rhs split into a list by comma
self.arglist = list of space-separated args (including '=' if it exists)

All args and list members are stripped of excess whitespace around the
strings, but case is preserved.
"""

class Page(default_cmds.MuxCommand):
    """
        Send a private message to another player.
    Usage:
        msg someone=message
    To page multiple folks:
        msg someone, someone_else, some_other_person=message
    To page-pose:
        msg someone=:some action.

    Options:
        /r               Reply to whoever paged you last.
        /ignore <user>   Ignore a character.
        /unignore <user> Unignore a character.
    """
    # these need to be specified

    key = "page"
    aliases = ["message", "mesg", "p", "pa", "pag", "msg"]
    locks = "cmd:all()"
    help_category = "General"

    def check_ignores(self, ref_list):
        targets = []
        for target in ref_list:
            ignore = target.db.page_ignore
            if not ignore:
                targets.append(target)
                continue
            if self.caller in ignore:
                self.caller.msg("%s is ignoring you." % target.name)
                continue
            else:
                targets.append(target)
        return targets
            

    def eliminate_sleepers(self, ref_list):
        targets = []
        for ref in ref_list:
            if ref.sessions:
                targets.append(ref)
            else:
                self.caller.msg("%s is not connected to the game right now." % ref.name)
        return targets

    def validate_targets(self, name_list, check_ignores=True):
        targets = []
        MAIN = 0
        for name in name_list:
            target = partial_pmatch(self.caller, name)
            try:
                if len(target) > 1:
                    raise IndexError
                target = target[0]
            except IndexError:
                self.caller.msg("I don't know a player named '%s'." % name)
                continue
            targets.append(target)
        if check_ignores:
            targets = self.check_ignores(targets)
        return targets

    def toggle_ignores(self, switch):
        """
        Toggle whether or not some folks are ignored.
        """
        if not self.args:
            return False
        targets = self.validate_targets(self.arglist, check_ignores=False)
        if not targets:
            self.caller.msg("No valid targets found.")
        if self.caller.db.page_ignore:
            ignore = self.caller.db.page_ignore
        else:
            ignore = []
        if switch:
            for target in targets:
                if target not in ignore:
                    ignore.append(target)
                    self.caller.msg("Ignoring %s." % target.name)
                else:
                    self.caller.msg("Already ignoring %s." % target.name)
        else:
            for target in targets:
                if target not in ignore:
                    self.caller.msg("You were not ignoring %s." % target.name)
                else:
                    ignore = [ person for person in ignore if person != target ]
                    self.caller.msg("No longer ignoring %s." % target.name)
        self.caller.db.page_ignore = ignore
        return True

    def switch_processor(self):
        """
        Handle command arguments.
        """
        if 'r' in self.switches:
            if self.caller.ndb.page_recent:
                self.targets = self.eliminate_sleepers(self.caller.ndb.page_recent)
            else:
                self.caller.msg("No one has paged you recently.")
            self.message = self.args
            return True
        if 'ignore' in self.switches:
            if not self.toggle_ignores(True):
                self.caller.msg("You must specify people you wish to ignore.")
            return False
        if 'unignore' in self.switches:
            if not self.toggle_ignores(False):
                self.caller.msg("You must specify folks you wish to unignore.")
            return False
        if self.rhs:
            self.message = self.rhs
        else:
            self.caller.msg("You must specify a message to send. Did you forget the = sign?")
            return False
        if self.lhslist:
            self.targets = self.eliminate_sleepers(self.validate_targets(self.lhslist))
        else:
            self.caller.msg("You must specify people to send the message to.")
        return True

    def posify(self, message):
        try:
            if message[0] == ':':
                message = message[1:]
                if message[0] in [':', ';', ',', "'" ]:
                    message = self.caller.name + message
                else:
                    message = self.caller.name + " " + message
            return message
        except IndexError:
            return message

    def send_message(self, message):
        """
        Does the actual paging.
        """
        targets = self.targets
        names = [ target.name for target in targets ]
        message = self.posify(message)
        message = "Message from %s to %s: %s" % (self.caller.name, ", ".join(names), message)

        # Make sure we get only one copy, and that it makes sense for one to be delivered at all.
        if self.caller not in targets and targets:
            self.caller.msg(message)

        for target in targets:
            target.msg(message)
            reply_list = [ person for person in targets if person != target ]
            reply_list.append(self.caller)
            target.ndb.page_recent = reply_list

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        MAIN = 0
        self.targets = []
        self.switches = [ switch.lower() for switch in self.switches ] #, bitches!

        if not self.switch_processor():
             return

        try:
            message = self.message
        except:
            message = self.rhs

        self.send_message(message)
