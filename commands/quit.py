"Quit command."
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from lib import fortunes
from random import choice

class Quit(default_cmds.MuxCommand):
    """
    quit

    Usage:
      quit

    Gracefully disconnect from the game.
    """
    key = "quit"
    locks = "cmd:all()"

    def func(self):
        "hook function"
        for session in self.caller.sessions:
            session.msg("{RQuitting{n\r%s" % choice(fortunes.FORTUNES))
            session.session_disconnect()
