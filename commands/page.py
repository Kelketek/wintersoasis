"""
Page command. Used to contact another player across the MUCK.
"""

from ev import default_cmds

from game.gamesrc.oasis.lib.oasis import partial_pmatch, check_ignores, check_sleepers, validate_targets


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
        Send a private message to another player.
    Usage:
        msg someone=message
    To page multiple folks:
        msg someone, someone_else, some_other_person=message
    To page-pose:
        msg someone=:some action.

    Options:
        /r               Reply to whoever paged you last.
    """
    # these need to be specified

    key = "page"
    aliases = ["message", "mesg", "p", "pa", "pag", "msg"]
    locks = "cmd:all()"
    help_category = "General"
    local_only = False
    message_format = "Message from %s to %s: %s"

    def switch_processor(self):
        """
        Handle command arguments.
        """
        if 'r' in self.switches:
            if self.caller.ndb.page_recent:
                self.targets = check_sleepers(self.caller, self.caller.ndb.page_recent)
            else:
                self.caller.msg("No one has paged you recently.")
            self.message = self.args
            return True
        if self.rhs:
            self.message = self.rhs
        else:
            self.caller.msg("You must specify a message to send. Did you forget the = sign?")
            return False
        if self.lhslist:
            self.targets = check_sleepers(self.caller, validate_targets(self.caller, self.lhslist, local_only=self.local_only))
        else:
            self.caller.msg("You must specify people to send the message to.")
        return True

    def posify(self, message):
        try:
            if message[0] == ':':
                message = message[1:]
                if message[0] in [':', ';', ',', "'" ]:
                    message = self.caller.name + message
                else:
                    message = self.caller.name + " " + message
            return message
        except IndexError:
            return message

    def send_message(self, message):
        """
        Does the actual paging.
        """
        targets = self.targets
        names = [ target.name for target in targets ]
        message = self.posify(message)
        message = self.message_format % (self.caller.name, ", ".join(names), message)

        # Make sure we get only one copy, and that it makes sense for one to be delivered at all.
        if self.caller not in targets and targets:
            self.caller.msg(message)

        for target in targets:
            target.msg(message)
            reply_list = [ person for person in targets if person != target ]
            reply_list.append(self.caller)
            target.ndb.page_recent = reply_list

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
         by the cmdhandler right after self.parser() finishes, and so has access
         to all the variables defined therein.
        """
        MAIN = 0
        self.targets = []
        self.switches = [ switch.lower() for switch in self.switches ] #, bitches!

        if not self.switch_processor():
             return

        try:
            message = self.message
        except:
            message = self.rhs

        self.send_message(message)

class Whisper(Page):
    """
    Whisper a message to someone in the room.
    """
    key = "whisper"
    aliases = ["whispe", "whisp", "whis", "whi", "wh"]
    locks = "cmd:all()"
    help_category = "General"
    local_only = True
    message_format = "%s whispers to %s: %s"
