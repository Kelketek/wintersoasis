"""
Senses commands. For stuff like taste, feel, and smell.
"""

from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from game.gamesrc.oasis.lib.constants import ALERT
from game.gamesrc.oasis.lib.oasis import validate_targets, check_ignores, check_owner

class Sense(default_cmds.MuxCommand):
    """
        Base command for Taste, Feel, and Smell.
    """
    key = 'sense'
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    verb = 'sense'
    verbed = 'sensed'

    def get_sense(self, target, prefix=False):
        if prefix:
            prefix = target.name + ': '
        else:
            prefix = ''
        try:
            self.caller.msg(prefix + target.db.senses[self.key] + '{n')
        except (TypeError, IndexError, KeyError):
            self.caller.msg('%sYou %s nothing special.{n' % (prefix, self.verb))
        target.msg(ALERT % '%s just %s you.' % (self.caller.name, self.verbed))

    def set_sense(self, target, message):
        if not (check_owner(self.caller, target) or target.access(self.caller, 'control')):
            self.caller.msg("{rPermission denied.{n")
            return
        try:
            target.db.senses[self.key] = self.rhs
        except TypeError:
            target.db.senses = { self.key : self.rhs }
        if not self.args:
            self.caller.msg('{cCleared.{n')
        else:
            self.caller.msg('{cSet.{n')

    def set_sense_handler(self):
        """
        Parse input for handling the 'set' version of sense.
        """
        match = self.caller.search(self.lhs)
        if not match:
            return
        self.set_sense(match, self.rhs)

    def func(self):
        """
        Determine whether we're sensing someone or something, or setting a sense.
        """
        self.switches = [ switch.lower() for switch in self.switches ]
        if 'set' in self.switches:
            self.set_sense_handler()
            return
        if 'here' in self.switches:
            targets = check_ignores(self.caller, self.caller.location.contents)
        else:
            if not self.args:
                self.caller.msg('You must specify a target.')
                return
            targets = validate_targets(self.caller, self.arglist)
        prefix = len(targets) > 1
        for target in targets:
            self.get_sense(target, prefix=prefix)

class Taste(Sense):
    """
    Reach out and lick someone!

    If you want to taste someone named Thaddius:
        taste Thaddius
    If you want to taste everything in the room:
        taste/here
    If you want to set your taste:
        taste/set me=It haz a flavr.
    """
    key = 'taste'
    verb = 'taste'
    verbed = 'tasted'

class Smell(Sense):
    """
    Depending on where you sniff, you may be shaking hands.

    If you want to smell someone named Thaddius:
        smell Thaddius
    If you want to smell everything in the room:
        smell/here
    If you want to set your scent:
        smell/set me=The funk of forty thousand years.
    """
    key = 'smell'
    verb = 'smell'
    verbed = 'smelled'

class Feel(Sense):
    """
    You should probably keep your paws to yourself, but...

    If you want to feel someone named Thaddius:
        feel Thaddius
    If you want to feel everything in the room:
        feel/here
    If you want to set your texture:
        feel/set me=Five O'clock shadow like 300 grain sandpaper.
    """
    key = 'feel'
    verb = 'feel'
    verbed = 'touched'
