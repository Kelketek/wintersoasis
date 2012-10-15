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
        Send a private message to another player:
        page someone=message
    """
    # these need to be specified

    key = "Msg"
    aliases = ["message", "mesg", "p", "pa", "pag", "page"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        MAIN = 0

        if not self.lhs:
            self.caller.msg("You must specify someone to page.")
            return
        if not self.rhs:
            self.caller.msg("You must specify a message to send. (Did you remember to include the = sign?)")
            return
        
        target = partial_pmatch(self.lhs)

        if not target or len(target) > 1:
            self.caller.msg("Couldn't find a player named " + self.lhs + ".")
            return
        target = target[MAIN]
        if not target.sessions:
            self.caller.msg(target.name + " is not connected to the game right now.")
            return
        target.msg("Message from " + self.caller.name + ": " + self.rhs)
        self.caller.msg("Message to " + target.name + ": " + self.rhs)
