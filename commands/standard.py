"""
Winter's Oasis standard command sets.
"""

from ev import CmdSet, Command
from ev import default_cmds
from src.commands.default import comms
from src.commands.default import unloggedin
from contrib.extended_room import CmdExtendedLook 
from game.gamesrc.oasis.commands import quote, character_commands, say, \
    page, warps, mail, ignore, lineeditor, senses, who, watch, hide_from, unloggedin, \
    quit

from contrib import menusystem
#from contrib import misc_commands
#from contrib import chargen

class ExampleCmdSet(CmdSet):
    """
    Implements an empty, example cmdset.
    """

    key = "ExampleSet"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        Here we just add the empty base Command object. It prints some info.
        """
        self.add(Command())


class DefaultCmdSet(default_cmds.CharacterCmdSet):
    """
    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_DEFAULT to point
    to this class.
    """
    key = "DefaultMUX"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_default
        super(DefaultCmdSet, self).at_cmdset_creation()
        self.add(quote.Quote())
        self.add(character_commands.WhoSpec())
        self.add(character_commands.Sheet())

        self.add(say.Say())
        self.add(say.Pose())
        self.add(say.Ooc())
        self.add(page.Page())
        self.add(page.Whisper())
        self.add(warps.Nexus())
        self.add(warps.IC())
        self.add(mail.Mail())
        self.add(ignore.Ignore())
        self.add(ignore.Unignore())
        self.add(senses.Taste())
        self.add(senses.Feel())
        self.add(senses.Smell())
        self.add(watch.Watch())
        self.add(watch.Unwatch())
        self.add(hide_from.HideFrom())
        self.add(hide_from.UnhideFrom())
        #
        # any commands you add below will overload the default ones.
        #
        self.add(menusystem.CmdMenuTest())
        self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    This is an example of how to overload the command set of the
    unloggedin commands, defined in
    src/commands/default/cmdset_unloggedin.py.

    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_UNLOGGEDIN to
    point to this class.
    """
    key = "Unloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_unloggedin
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(unloggedin.Connect())
        self.add(unloggedin.Magic())
        self.add(who.Who())

class OOCCmdSet(default_cmds.PlayerCmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "OOC"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_ooc
        super(OOCCmdSet, self).at_cmdset_creation()
        self.remove(comms.CmdPage())
        self.add(quit.Quit())
        self.add(who.Who())
        #
        # any commands you add below will overload the default ones.
        #
