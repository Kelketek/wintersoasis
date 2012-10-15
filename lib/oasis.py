import ev
from constants import *
from ev import utils
from src.server.sessionhandler import SESSIONS

def partial_pmatch(name):
    """
        Feed this a name, and it will return character matches. It will return only
    one match if the name is exact, and it will return multiple if there are multiple
    people online who match, but none of which are exact matches.
        All results are returned in a list. An empty list is returned if there is no match.
    """
    target = NEXUS.search("*" + name, global_search = True)
    if target:
        return [ target ]
    matches = []
    for session in SESSIONS.sessions.values():
        if session.get_character().name.lower().startswith(name.lower()):
            matches.append(session.get_character())
    return matches
