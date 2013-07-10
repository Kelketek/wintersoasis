"""
Common functions used by other commands in the Winter's Oasis command sets.
"""
import ev
import settings
import time
from constants import *
from ev import utils
from src.server.sessionhandler import SESSIONS
from twisted.internet import reactor

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

CHARACTER = 0
TIMESTAMP = 1

def partial_pmatch(me, name, local_only=False):
    """
        Feed this a name, and it will return character matches. It will return
    only one match if the name is exact or unambiguous, and it will return
    multiple if there are multiple people online who match, but none of which
    are exact matches. All results are returned in a list. An empty list is
    returned if there is no match.
        Me is the object that will be returned if the query is 'me'.
    """
    if local_only:
        target = []
        targets = me.search(name, ignore_errors=True)
        if type(targets) == list:
            for thing in targets:
                if utils.inherits_from(thing, settings.BASE_CHARACTER_TYPECLASS):
                    target.append(thing)
        elif not targets:
            pass
        else:
            target.append(targets)
        return target
    else:
        try:
            # In case user explicitely indicates a ref.
            if name[0] in [ '*', '#' ]:
                global_name = name
            else:
                global_name = '*' + name
        except IndexError:
            pass
        target = me.search(global_name, global_search=True, quiet=True, use_nicks=True)
    if target:
        if type(target) == list:
            return target
        else:
            return [ target ]
    matches = []
    for session in SESSIONS.sessions.values():
        character = session.get_character()
        if character and character.name.lower().startswith(name.lower()):
            matches.append(character)
    return matches

def action_watchers(user, function, kwargs, delay=0, respect_hide=True):
    """
    Perform an action for all followers. Delay is ignored for Wizards.
    """
    online_users = [ session.get_character() for session in SESSIONS.sessions.values() if session.get_character() ]
    for target in online_users:
        if target.check_list(user, "watching"):
            kwargs['target'] = target
            kwargs['user'] = user
            if user.locks.check_lockstring(target, 'admin:perm(Wizards)'):
                function(**kwargs)
            elif respect_hide and check_hiding(target, [user]):
                reactor.callLater(delay, function, **kwargs)

def toggle_notifications(user, key, toggle):
    """
    Toggles whether or not a user gets messages identified by a certain key.
    """
    ignored_messages = user.db.ignored_message_keys
    if not ignored_messages:
        ignored_messages = []
    if toggle:
        ignored_messages = [ notification for notification in ignored_messages if notification != key.lower() ]
    else:
        if key.lower() in ignored_messages:
            return
        else:
            ignored_messages.append(key.lower())
    user.db.ignored_message_keys = ignored_message_keys

def ignored_notifications(user):
    """
    Returns a list of message keys the user is ignoring.
    """
    if not user.db.ignored_message_keys:
        return []
    else:
        return user.db.ignored_message_keys

def check_sleepers(person, ref_list, silent=False):
    targets = []
    for ref in ref_list:
        if ref and ref.player:
            targets.append(ref)
        else:
            if not silent:
                person.msg("%s is not connected to the game right now." % ref.name)
    return targets

def check_ignores(person, ref_list, silent=False):
    """
        Check a list and eliminate all characters within it that are ignoring a
    person.
    """
    # We don't ignore administrators.
    if person.locks.check_lockstring(person, 'admin:perm(Wizards)'):
        return ref_list
    targets = []
    for target in ref_list:
        ignore = target.db.ignore
        if not ignore:
            ignore = []
        if person in ignore:
            if not silent:
                person.msg("%s is ignoring you." % target.name)
            continue
        else:
            targets.append(target)
    return targets

def check_hiding(person, ref_list):
    """
    Remove players from a reflist who are hiding from a person or in general.
    """
    return [ item for item in ref_list if (not item.db.hiding) and (not person in item.db.hiding_from) ]

def validate_targets(person, name_list, ignores=True, local_only=True, silent=False):
    """
        Check a list and eliminate all targets that don't exist.
    """
    targets = []
    MAIN = 0
    for name in name_list:
        target = partial_pmatch(person, name, local_only=local_only)
        try:
            if len(target) > 1:
                raise IndexError
            target = target[0]
        except IndexError:
            if not silent:
                if local_only:
                    person.msg("There's no one here named '%s'." % name)
                else:
                    person.msg("I don't know a character named '%s'." % name)
            continue
        targets.append(target)
    if ignores:
        targets = check_ignores(person, targets, silent=silent)
    return targets
