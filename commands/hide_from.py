"""
    Hide command. Adds or removes other characters from a character's hide
list, or allows a character to hide from everyone.
"""

from ev import default_cmds
from game.gamesrc.oasis.lib.oasis import validate_targets

class HideFrom(default_cmds.MuxCommand):
    """
        Become less visible to another player or all players. Keeps you from
    showing up in other people's 'following' lists and other subtle exclusions.

    For instance, to hide from someone named Thaddius:
        hidefrom Thaddius
    You can hide from multiple people by separating their names with commas;
        hidefrom Thaddius, Phoebe
    You can hide from everyone with:
        hidefrom/all
    """
    # these need to be specified

    key = "hidefrom"
    aliases = ['hf']
    locks = "cmd:all()"
    help_category = "General"
    hiding = True

    def toggle_hiding(self, switch):
        """
        Toggle whether or not some folks are hidden from.
        """
        targets = validate_targets(self.caller, self.arglist, ignores=False, local_only=False)
        if not targets:
            self.caller.msg("No valid targets found.")
            return
        hiding_from = self.caller.db.hiding_from
        if switch:
            for target in targets:
                if target not in hiding_from:
                    hiding_from.append(target)
                    self.caller.msg("Hiding from %s." % target.name)
                else:
                    self.caller.msg("Already hiding from %s." % target.name)
                if target.locks.check_lockstring(target, 'admin:perm(Wizards)'):
                    self.caller.msg('{rWARNING: %s is an administrator. Hiding is futile.{n' % target.name)
        else:
            for target in targets:
                if target not in hiding_from:
                    self.caller.msg("You were not hiding from %s." % target.name)
                else:
                    hiding_from = [ person for person in hiding_from if person != target ]
                    self.caller.msg("No longer hiding from %s." % target.name)
        self.caller.db.hiding_from = hiding_from

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        MAIN = 0
        if not self.args:
            self.caller.msg('You must specify someone.')
        self.toggle_hiding(self.hiding)
        
        

class UnhideFrom(HideFrom):
    """
    Stop hiding from a previously hidden from player.

    To stop hiding from someone named Thaddius:
        unhide Thaddius
    You can hide from several people by separating their names with commas:
        unhide Thaddius, Phoebe
    If you've hidden from everyone, you can unhide with:
        unhide/all
    """
    key = "unhidefrom"
    aliases = ['uhf']
    locks = "cmd:all()"
    help_category = "General"
    hiding = False
