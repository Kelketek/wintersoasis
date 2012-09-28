"""
Example command module template

Copy this module up one level to gamesrc/commands/ and name it as
befits your use.  You can then use it as a template to define your new
commands. To use them you also need to group them in a CommandSet (see
examples/cmdset.py)

"""

import time
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from settings import *


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

class WhoSpec(default_cmds.MuxCommand):
    """
        Whospecies looks up all players in the room and grabs their name, sex,
    and species.

    """
    # these need to be specified

    key = "whospecies"
    aliases = ["ws", "whos", "whospec"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        characters = [ thing for thing in self.caller.location.contents
            if thing.player
        ]

        if "far" in self.switches:
	    characters = [ thing for thing in
	        self.caller.search(self.args, global_search=True, ignore_errors=True)
		if thing.player
	    ]

        idle_threshhold = 180 # Three minutes minimum idle.

        self.caller.msg("+-Stat---Name------------------Sex---------Species-----------------+")
        for character in characters:
	    if character.sessions:
	        idle_time = time.time() - character.sessions[0].cmd_last_visible
		if idle_time > idle_threshhold:
		    name = name = character.name + "[Idle " + utils.time_format(idle_time,1) + "]"
		else:
		    name = character.name
            else:
	        name = character.name + "[Zzz]"

	    status = character.db.status
	    if not status:
	        status = ""
            line = "| %-5s| %-20s| %-10s| %-24s|" % ( character.db.status, name, character.db.sex, character.db.species )
            self.caller.msg(line)
        self.caller.msg("+------------------------------------------------------------------+")
