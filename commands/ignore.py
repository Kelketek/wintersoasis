"""
    Ignore command. Adds or removes other characters from a character's ignore
list.
"""

import time
from ev import Command as BaseCommand
from ev import default_cmds
from game.gamesrc.oasis.lib.oasis import partial_pmatch, check_ignores, validate_targets

class Ignore(default_cmds.MuxCommand):
    """
        Opt out of messages from an individual. Note: This may not work for all commands, and may be limited in other commands.

    For instance, to ignore someone named 'Thaddius':
        ignore Thaddius
    You can ignore multiple people by separating their names with commas;
        ignore Thaddius, Phoebe
    """
    # these need to be specified

    key = "ignore"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"
    ignoring = True

    def toggle_ignores(self, switch):
        """
        Toggle whether or not some folks are ignored.
        """
        targets = validate_targets(self.caller, self.arglist, ignores=False, local_only=False)
        if not targets:
            self.caller.msg("No valid targets found.")
            return
        ignore = self.caller.db.ignore
        if switch:
            for target in targets:
                if target not in ignore:
                    ignore.append(target)
                    self.caller.msg("Ignoring %s." % target.name)
                else:
                    self.caller.msg("Already ignoring %s." % target.name)
                if target.locks.check_lockstring(target, 'admin:perm(Wizards)'):
                    self.caller.msg('{rWARNING: Your ignore will be null as long as %s is an administrator.{n' % target.name)
        else:
            for target in targets:
                if target not in ignore:
                    self.caller.msg("You were not ignoring %s." % target.name)
                else:
                    ignore = [ person for person in ignore if person != target ]
                    self.caller.msg("No longer ignoring %s." % target.name)
        self.caller.db.ignore = ignore

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        MAIN = 0
        if not self.args:
            self.caller.msg('You must specify someone.')
        self.toggle_ignores(self.ignoring)
        
        

class Unignore(Ignore):
    """
    Stop ignoring a previously ignored player.

    To forgive someone named 'Thaddius':
        unignore Thaddius
    You can unignore several people by separating their names with commas:
        unignore Thaddius, Phoebe
    """
    key = "unignore"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"
    ignoring = False
