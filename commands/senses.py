"""
Senses commands. For stuff like taste, feel, and smell.
"""

from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from game.gamesrc.oasis.lib.constants import ALERT
from game.gamesrc.oasis.lib.oasis import validate_targets, check_ignores

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
            self.caller.msg('%s{cYou %s nothing special.{n' % (prefix, self.verb))
        target.msg('{c%s just %s you.{n' % (self.caller.name, self.verbed))

    def set_sense(self):
        try:
            self.caller.sb.senses[self.key] = self.args
        except TypeError:
            self.caller.sb.senses = { self.key : self.args }
        if not args:
            self.caller.msg('{cCleared.{n')
        else:
            self.caller.msg('{cSet.{n')

    def func(self):
        """
        Determine whether we're sensing someone or something, or setting a sense.
        """
        self.switches = [ switch.lower() for switch in self.switches ]
        if 'set' in self.switches:
            self.set_sense()
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
    Taste stuff. 
    """
    key = 'taste'
    verb = 'taste'
    verbed = 'tasted'

class Smell(Sense):
    """
    Smell stuff.
    """
    key = 'smell'
    verb = 'smell'
    verbed = 'smelled'

class Feel(Sense):
    """
    Feel stuff.
    """
    key = 'feel'
    verb = 'feel'
    verbed = 'touched'
