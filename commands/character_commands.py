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

class Sheet(default_cmds.MuxCommand):
    """
    +sheet looks up the character information of your character. You can use
the /bg switch to get the background of your character.

    Priviledged users can give a player's name as an argument to this command
and get their info.
    """
    key = "sheet"
    locks = "cmd:all()"
    help_category = "Character"

    def display_sheet(self,char):
       """
       Displays a character sheet.
       """
       if not char.db.stats:
           stat_dict = { }
       else:
           stat_dict = char.db.stats
       self.caller.msg(char.name + ", the " + str(char.db.sex) + " " + str(char.db.species) + ":")
       self.caller.msg("")

       for key, value in stat_dict.items():
            self.caller.msg("{c%-11s: {y%s" % (key, str(value)))

       self.caller.msg("")

       if char.db.qualities:
           for key, value in char.db.qualities.items():
                line = "{c%-20s{b: {g%s{n" % (key, value)
                self.caller.msg(line)

    def display_background(self, char):
        """
	Displays a character's background.
	"""
	self.caller.msg("The legend of " + char.name + ":")
	self.caller.msg("")
	background = char.db.background
	if not background:
	    self.caller.msg("    This tale is not written.")
            return
        self.caller.msg(background)

    def func(self):
        """
	Primary function for +sheet.
	"""
	self.caller.msg("")
	if self.args:
	    if not (self.caller.check_permstring("Immortals") or self.caller.check_permstring("Wizards")
	    or self.caller.check_permstring("PlayerHelpers")):
	        self.caller.msg("Players cannot look at each other's sheets.")
	        return
	    char_list = self.caller.search(self.args, global_search=True, ignore_errors=True)
	    if char_list:
	        char = char_list[0]
	    else:
	        self.caller.msg("No such character: " + self.args)
		self.caller.msg("")
	else:
	    char = self.caller
	if "bg" in self.switches:
	    self.display_background(char)
	    self.caller.msg("")
	    return
        self.display_sheet(char)
	self.caller.msg("")

class WhoSpec(default_cmds.MuxCommand):
    """
        Whospecies looks up all players in the room and grabs their name, sex,
    species, and status. You can use the /far switch to look up a remote player.

    For instance,

    ws/far Thaddius

    ...will look up Thaddius's name, sex, species, and status.

    """
    # these need to be specified

    key = "whospecies"
    aliases = ["ws", "whos", "whospec"]
    locks = "cmd:all()"
    help_category = "Character"

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

        self.caller.msg("+-Stat---Name----------------------------Sex---------Species-----------------+")
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
            line = "| %-5s| %-30s| %-10s| %-24s|" % ( character.db.status, name, character.db.sex, character.db.species )
            self.caller.msg(line)
        self.caller.msg("+----------------------------------------------------------------------------+")
