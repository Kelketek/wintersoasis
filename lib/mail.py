"""
Library for in-game mail functions.
"""
import time
from string import Template
from django.core.urlresolvers import reverse
from twisted.mail.smtp import sendmail
from twisted.internet.defer import Deferred
from twisted.internet import reactor

from cgi import escape
from email import Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate

import ev
import settings
import src.utils
from constants import *
from src.utils import create

MESSAGE = 0
TIMESTAMP = 1

class Mail:
    """
        Creates a wrapper around a stored mail message to make more easily
    manipulated for mail purposes.
    """
    def __init__(self, message):
       message, timestamp, read = message
       self.message = message
       self.subject = message.header
       self.senders = [ character.typeclass for character in message.senders if int(character.dbobj.date_created.strftime('%s')) <= int(timestamp.strftime('%s')) ]
       self.recipients = [ character.typeclass for character in message.receivers if int(character.dbobj.date_created.strftime('%s')) <= int(timestamp.strftime('%s')) ]
       self.sent_at = timestamp
       self.sender_names = ', '.join([ sender.name for sender in self.senders ])
       self.recipient_names =  ', '.join([ recipient.name for recipient in self.recipients ])
       # Bogus temporary values
       self.read_at = time.time()
       self.replied_at = time.time()
       self.sender_deleted_at = time.time()
       self.recipient_deleted_at = time.time()
       self.get_absolute_url = reverse('messages_detail', args=[self.message.id])
       if read:
           self.new = False
       else:
           self.new = True

def get_messages(character):
    """
    Get the raw messages for a user.
    """
    mail = character.db.mail
    print mail
    try:
        messages = [item for item in mail if item[TIMESTAMP] <= item[MESSAGE].date_sent]
        # Let's clean up mail storage for this user while we're at it.
        character.db.mail = messages
    except TypeError:
        messages = []
    return messages

def get_inbox(character):
    """
    Get the messages for a user, stripped of stamps.
    """
    messages = get_messages(character)
    return [ Mail(message) for message in messages ]


def send_message(senders, subject, body, receivers, priority=False, silent_send=False, silent_receive=False, send_email=False):
    """
    Send a mail message to specified recipients. (Deprecated. Will be removed soon)
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
    receivers = [ receiver for receiver in message.receivers if receiver.player.user.email ]
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

    print "Starting send..."
    for receiver in receivers:
        msg['To'] = receiver.db.email
        sendmail(SMTP_HOST, MAIL_FROM, receiver.player.user.email, msg.as_string())


