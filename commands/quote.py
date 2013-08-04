"""
Example command module template

Copy this module up one level to gamesrc/commands/ and name it as
befits your use.  You can then use it as a template to define your new
commands. To use them you also need to group them in a CommandSet (see
examples/cmdset.py)

"""

from ev import Command as BaseCommand
from ev import default_cmds
from ev import syscmdkeys
from ev import CmdSet

CMD_NOMATCH = syscmdkeys.CMD_NOMATCH
CMD_NOINPUT = syscmdkeys.CMD_NOINPUT

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own
    command styles. Note that Evennia's default commands
    use MuxCommand instead (next in this module)

    Note that the class's __doc__ string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    """
    # these need to be specified

    key = "MyCommand"
    aliases = ["mycmd", "myc"]
    locks = "cmd:all()"
    help_category = "General"

    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.


    # (we don't implement hook method access() here, you don't need to
    #  modify that unless you want to change how the lock system works
    #  (in that case see src.commands.command.Command))

    def at_pre_cmd(self):
        """
        This hook is called before self.parse() on all commands
        """
        pass

    def parse(self):
        """
        This method is called by the cmdhandler once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from self.func() (see below)

        The following variables are available to us:
           # class variables:

           self.key - the name of this command ('mycommand')
           self.aliases - the aliases of this cmd ('mycmd','myc')
           self.locks - lock string for this command ("cmd:all()")
           self.help_category - overall category of command ("General")

           # added at run-time by cmdhandler:

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following self.cmdstring.
           self.cmdset - the cmdset from which this command was picked. Not
                         often used (useful for commands like 'help' or to
                         list all available commands etc)
           self.obj - the object on which this command was defined. It is often
                         the same as self.caller.
        """
        pass

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        self.caller.msg("Command called!")

    def at_post_cmd(self):
        """
        This hook is called after self.func().
        """
        pass


class MuxCommand(default_cmds.MuxCommand):
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

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the cmdhandler right after self.parser() finishes, and so has access
        to all the variables defined therein.
        """
        # this can be removed in your child class, it's just
        # printing the ingoing variables as a demo.
        super(MuxCommand, self).func()

class QuoteCmdSet(CmdSet):
    """CmdSet for the editor commands"""
    key = "quotecmdset"
    mergetype = "Replace"
    priority = 11
    no_objs = True
    no_exits = True
    no_channels = True
    key_mergetype = {'quotecmdset','Replace'}

class AddLine(MuxCommand):
    """No command match - Inputs line of text into the buffer."""
    key = CMD_NOMATCH
    aliases = [CMD_NOINPUT]
    MAX_LENGTH = 255

    def func(self):
        "Adds the line without any formatting changes."
        if len(self.caller.ndb._quoter.buffer) > AddLine.MAX_LENGTH:
             self.caller.msg("Buffer full! Use .end or .abort!")
             return
        if not self.args:
            buf = "\n"
        else:
            buf = self.args
        self.caller.ndb._quoter.addline(buf)

class Aborter(MuxCommand):
    """Abort command for the quote utility."""
    key = ".abort"
    aliases = []
    locks = "cmd:all()"
    
    def func(self):
        self.caller.msg("Aborted.")
        self.caller.ndb._quoter.quit(self.caller)
       
class Ender(MuxCommand):
    """Finishes quote input and sends the contents to the room."""
    key = ".end"
    aliases = []
    locks = "cmd:all()"

    def func(self):
        if not self.caller.ndb._quoter.buffer:
            self.caller.msg("Aborted. No lines in buffer.")
        else:
            self.caller.location.msg_contents("<Quote from %s>" % self.caller.name)
            # Actually send the quote.
            self.caller.ndb._quoter.send_quote(self.caller)
            self.caller.location.msg_contents("<End Quote>")
            self.caller.ndb._quoter.quit(self.caller)

class Quoter(object):
    """
    This is used as the main object for the quote utility. It provides a very limited
    command set where only a few keys can be used to do anything. Namely, .end or .abort.
    This command is used instead of the line editor when one wants to not make things too
    complicated.
    """

    def __init__(self, caller):
        quote_cmdset = QuoteCmdSet()
        quote_cmdset.add(Ender)
        quote_cmdset.add(Aborter)
        quote_cmdset.add(AddLine)
        caller.cmdset.add(quote_cmdset)
        caller.msg("Enter the text you want to past now. Type '.end' when you are finished, or '.abort' to cancel.")
        caller.ndb._quoter = self
        self.buffer = []

    def addline(self, line):
        self.buffer.append(line)

    def send_quote(self, caller):
        caller.location.msg_contents("\r\n".join(caller.ndb._quoter.buffer))

    def quit(self, caller):
        "Cleanly exit the quoter."
        del caller.ndb._quoter
        caller.cmdset.delete(QuoteCmdSet)



class Quote(MuxCommand):
    """
    Simple command example

    Usage: 
      quote <text>

    This command simply echoes text to the room.
    """

    key = "quote"
    aliases = ["paste", "@quote", "@paste"] 
    locks = "cmd:all()"

    def func(self):
        Quoter(self.caller)
