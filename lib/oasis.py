"""
Common functions used by other commands in the Winter's Oasis command sets.
"""
import ev
import settings
import time
from cgi import escape
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
from string import Template
from twisted.mail.smtp import sendmail
from constants import *
from ev import utils
from src.utils import create
from src.server.sessionhandler import SESSIONS
from src.comms.models import Msg
from twisted.internet.defer import Deferred
from twisted.internet import reactor

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
        target = me.search(global_name, global_search=True, ignore_errors=True)
    if target:
        if type(target) == list:
            return target
        else:
            return [ target ]
    matches = []
    if local_only:
        return matches
    for session in SESSIONS.sessions.values():
        character = session.get_character()
        if character and character.name.lower().startswith(name.lower()):
            matches.append(character)
    return matches

def object_stamp(thing):
    """
        Create an 'object stamp'-- this is a tuple for storage of an object
    refrence and the current time. Useful for seeing if the object ref has been
    recycled since the item was stored.
    """
    return (thing, time.time())

def in_object_list(thing, object_list):
    """
    Take an object stamp and determine whether or not it exists in a specified list.
    """
    target = current_object(thing)
    if target in distill_list(object_list):
        return target

def ferment_list(ref_list):
    """
    Converts a list of dbrefs into a list of object_stamps
    """
    return [ object_stamp(dbref) for dbref in ref_list if dbref ]

def distill_list(object_list, preserve_format=False):
    """
        Take a list of object stamps and return the objects that are legit.
    The preserve_format flag is for retaining the character stamp format instead
    of just returning a list of characters.
    """
    if not object_list:
        object_list = []
    if preserve_format:
        return [ thing for thing in object_list if current_object(thing) ]
    else:
        return [ current_object(thing) for thing in object_list if current_object(thing) ]

def current_object(thing):
    """
        Takes an object stamp and returns the object if that
    object was made before or on its time stamp.
    """
    thing, timestamp = thing
    
    if not thing:
        return
    if timestamp >= int(thing.dbobj.date_created.strftime('%s')):
        return thing
    else:
        return

def check_follow(user, target, ignores=True):
    """
    Checks to see if user follows target.
    """
    CHARACTER = 0
    TIMESTAMP = 1
    following = user.db.following
    if not following:
        return False
    following = [ current_object(thing) for thing in following if current_object(thing) ]
    if target in following:
        if ignores:
            if not check_ignores(target, [user], silent=True):
                return False
        return True

def action_followers(user, function, kwargs, delay=0, respect_hide=True):
    """
        Perform an action for all followers. Delay is ignored for Wizards.
    """
    online_users = [ session.get_character() for session in SESSIONS.sessions.values() if session.get_character() ]
    for target in online_users:
        if check_follow(target, user):
            kwargs['target'] = target
            kwargs['user'] = user
            if target.locks.check_lockstring(target, 'admin:perm(Wizards)'):
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

def send_message(senders, subject, body, receivers, priority=False, silent_send=False, silent_receive=False, send_email=False):
    """
    Send a mail message to specified recipients.
    """
    message = create.create_message(senderobj=senders, message=body,
           receivers=receivers, header=subject)
    successful = []
    for target in receivers:
        try:
            if len(target.db.mail) >= MAX_MESSAGES and not priority:
                if not silent_send:
                    for sender in senders:
                        sender.msg(ALERT % "Mailbox of %s is full. Could not send message!" % target.name)
                continue
            target.db.mail.append([message, message.date_sent, False])
        except (TypeError, AttributeError):
            target.db.mail = [ [message, message.date_sent, False] ]
        if not silent_receive:
            target.msg(ALERT % "You have new mail! Check it by typing: mail")
        successful.append(target)
    if EMAIL and send_email:
        send_email_copy(message)
    return successful

def send_email_copy(message):
    """
    Sends an email copy of a message to all relevant targets.
    """
    receivers = [ receiver for receiver in message.receivers if receiver.db.email ]
    subject = message.header
    body = message.message
    if not (receivers):
        return

    msg = MIMEMultipart('alternative')
    msg['From'] = "Winter's Oasis <messages@wintersoasis.com>"
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    # HTML email part.
    html_part = MIMEText('text', 'html')
    html_source = Template(HTML_TEMPLATE)
    value_map = {
        'from' : ', '.join([ sender.name for sender in message.senders ]),
        'message' : escape(unicode(body)).replace('\n', '<br />'),
        'recipients' : ', '.join([ receiver.name for receiver in message.receivers ]) }
    html_part.set_payload(html_source.substitute(value_map))

    value_map['message'] = unicode(body)
    text_source = Template(TEXT_TEMPLATE)
    body = text_source.substitute(value_map)
    text_part = MIMEText(unicode(body), 'plain', 'utf-8')
    msg.attach(text_part)
    msg.attach(html_part)

    for receiver in receivers:
        msg['To'] = receiver.db.email
        sendmail(SMTP_HOST, MAIL_FROM, receiver.db.email, msg.as_string())

def check_sleepers(person, ref_list, silent=False):
    targets = []
    for ref in ref_list:
        if ref.sessions:
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
        ignore = distill_list(target.db.ignore)
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
    return [ item for item in ref_list if (not item.db.hiding) and (not person in distill_list(item.db.hiding_from)) ]

def check_owner(person, target):
    """
    Checks to see if a user owns an object.
    """
    owner = target.db.owner
    if not owner:
        return False
    return person == current_object(owner)

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
