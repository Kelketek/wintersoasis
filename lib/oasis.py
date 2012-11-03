import ev
from ev import utils
import settings
from src.server.sessionhandler import SESSIONS

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
        for thing in targets:
            if utils.inherits_from(thing, settings.BASE_CHARACTER_TYPECLASS):
                target.append(thing)
    else:
        target = me.search("*" + name, global_search=True, ignore_errors=True)
    if target:
        if type(target) == list:
            return target
        else:
            return [ target ]
    matches = []
    if local_only:
        return matches
    for session in SESSIONS.sessions.values():
        if session.get_character().name.lower().startswith(name.lower()):
            matches.append(session.get_character())
    return matches

def create_mail(senderobj, message, channels=None,
                   receivers=None, locks=None, title=None):
    """
        Mail message. This is based on the Msg class, and will likely become
    distinct as development progresses.
    """
    if not message:
        # we don't allow empty messages.
        return
    new_message = Mail(db_message=message)
    new_message.save()
    for sender in make_iter(senderobj):
        new_message.senders = sender
    new_message.title = title
    for channel in make_iter(channels):
        new_message.channels = channel
    for receiver in make_iter(receivers):
        new_message.receivers = receiver
    if locks:
        new_message.locks.add(locks)
    new_message.save()
    return new_message

