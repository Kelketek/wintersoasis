"""
Example command module template

Copy this module up one level to gamesrc/commands/ and name it as
befits your use.  You can then use it as a template to define your new
commands. To use them you also need to group them in a CommandSet (see
examples/cmdset.py)

"""
import time
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils
from game.gamesrc.oasis.lib.oasis import check_ignores
from src.server.sessionhandler import SESSIONS

class Who(default_cmds.MuxCommand):
    """
    List all players, their locations, online times, idle times, and more.

    Usage:
        WHO
    Wizards can do this to get more information:
        WHO/wiz
    """
    key = "who"
    aliases = ["findall", "fa", "wa", "whereare"]
    locks = "cmd:perm(Immortals)"
    help_category = "General"

    # Each of these takes a list of lists. The first element in each list
    # should be the session object. After that should be the string in
    # progress. Each section adds to the string.

    SESSION = 0
    STRING = 1

    def get_status(self, session):
        status = session.get_character().db.status
        if not status:
            return ''
        return status
    get_status.title = "Status"
    get_status.spacing = 8
    get_status.color = '{r'

    def get_location(self, session):
        location = session.get_character().location
        if location and self.admin:
            return '%s(#%s)' % ( location, location.dbobj.id )
        return location
    get_location.title = "Location"
    get_location.spacing = 20
    get_location.color = '{w'

    def get_online_time(self, session):
        FULL = 1
        online_time = time.time() - session.conn_time
        return utils.time_format(online_time, FULL)
    get_online_time.title = "On For"
    get_online_time.spacing = 8
    get_online_time.color = '{M'

    def get_idle_time(self, session):
        PARTIAL = 0
        delta_cmd = time.time() - session.cmd_last_visible
        return utils.time_format(delta_cmd, PARTIAL)
    get_idle_time.title = "Idle"
    get_idle_time.spacing = 8
    get_idle_time.color = '{y'

    def get_ip(self, session):
        return session.address[0]
    get_ip.title = "IP"
    get_ip.spacing = 13
    get_ip.color = '{B'

    def get_doing(self, session):
        doing = session.get_character().db.doing
        if not doing:
            return ''
        return doing
    get_doing.title = "Doing..."
    get_doing.spacing = 0
    get_doing.color = '{c'

    def get_name(self, session):
        character = session.get_character()
        name = character.name
        if self.admin:
            name += '(#%s)' % character.dbobj.id
        return name
    get_name.title = "Name"
    get_name.spacing = 20
    get_name.color = '{G'

    def func(self):
        """
        Contructs the desired loop based on switches.
        """
        construction = [ self.get_name, self.get_online_time, self.get_idle_time, self.get_status, self.get_location ]
        self.switches = [ switch.lower() for switch in self.switches ]
        if 'wiz' in self.switches and self.caller.locks.check_lockstring(self.caller, 'admin:perm(Immortals)'):
            construction.append(self.get_ip)
            self.admin = True
        else:
            construction.append(self.get_doing)
            self.admin = False
        header = ''
        separator = ' '
        for function in construction:
             header += '%s%s{n' % (function.color, function.title)
             padding = function.spacing - len(function.title)
             header += separator * padding
        self.caller.msg(header)
        users = [ [session, ''] for session in SESSIONS.get_sessions() if check_ignores(self.caller, [session.get_character()], silent=True) ]
        for user in users:
             for function in construction:
                 user[Who.STRING] += function.color + "%%-%ss" % function.spacing % function(user[Who.SESSION]) + '{n'
             self.caller.msg(user[Who.STRING])
