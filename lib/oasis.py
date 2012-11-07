import ev
import settings
import smtplib
from cgi import escape
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
from string import Template
from ev import utils
from src.server.sessionhandler import SESSIONS
from src.comms.models import Msg

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

def send_game_mail(message):
    """
    Sends mail from one player to another.
    """
    sender = message.senders[0].name
    receivers = [ receiver for receiver in message.receivers if receiver.db.email ]
    subject = message.header
    body = message.message
    if not (receivers):
        return

    HOST = 'localhost'
    msg = MIMEMultipart('alternative')
    msg['From'] = "Winter's Oasis <messages@wintersoasis.com>"
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    # HTML email part.
    html_part = MIMEText('text', 'html')
    html_source = Template("""
<html>
<body>
You have a new message from <strong>${from}</strong> to <strong>${recipients}</strong>:<br />

<p>${message}</p>

To check and manage your in-game messages, log in! :D
</body>
</html>
""")
    value_map = { 'from' : sender, 'message' : escape(unicode(body)), 'recipients' : ', '.join([ receiver.name for receiver in receivers ]) }
    html_part.set_payload(html_source.substitute(value_map))

    text_source = Template("""
You have a new message from ${from} to ${recipients}:

${message}

To check and manage your in-game messages, log in! :D
""")
    body = text_source.substitute(value_map)
    text_part = MIMEText(unicode(body), 'plain', 'utf-8')
    msg.attach(text_part)
    msg.attach(html_part)

    server = smtplib.SMTP(HOST)
    for receiver in receivers:
        msg['To'] = receiver.db.email
        server.sendmail('messages@wintersoasis.com', receiver.db.email, msg.as_string())
    server.quit()

    server.close()
