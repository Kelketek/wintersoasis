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

    locks = "cmd:all()"

    def func(self):
        "hook function"
        player = self.caller.player

        fortune = choice(fortunes.FORTUNES)

        if 'all' in self.switches:
            player.msg("{RQuitting{n all sessions. Hope to see you soon again.\r%s" % fortune, sessid=self.sessid)
            for session in player.get_all_sessions():
                player.disconnect_session_from_player(session.sessid)
        else:
            nsess = len(player.get_all_sessions())
            if nsess == 2:
                player.msg("{RQuitting{n. One session is still connected.\r%s" % fortune, sessid=self.sessid)
            elif nsess > 2:
                player.msg("{RQuitting{n. %i session are still connected.\r%s" % (nsess-1, fortune), sessid=self.sessid)
            else:
                # we are quitting the last available session
                player.msg("{RQuitting{n.\r%s" % fortune, sessid=self.sessid)
            player.disconnect_session_from_player(self.sessid)
