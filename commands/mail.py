#!/usr/bin/env python
import ev
from ev import Command as BaseCommand
from ev import default_cmds
from src.utils import create, utils
from game.gamesrc.oasis.lib.oasis import partial_pmatch, send_game_mail

class Mail(default_cmds.MuxCommand):
    """
    Send a mail message to another player.
    """
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
    key = "mail"
    aliases = []
    locks = "pperm(Immortals)"
    help_category = "General"

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the cmdhandler right after self.parser() finishes, and so has access
        to all the variables defined therein.
        """
        if not (self.lhs and self.rhs):
            self.caller.msg("Usage: mail person=subject\nAn editor will be launched to allow you to set the body.")
            return
        self.switches = [ switch.lower() for switch in self.switches ]
        if 'quick' in self.switches:
            subject = 'Quick message from %s' % self.caller.name
            body = self.rhs
            target = partial_pmatch(self.caller, self.lhs)
            if len(target) > 1 or not target:
                self.caller.msg("I don't recognize a character named '%s'" % self.lhs)
                return
            target = target[0]
            message = create.create_message(self.caller, body,
                   receivers=[target], header=subject)
            target.db.new_message=message
            
            #send_game_mail(message)
    
