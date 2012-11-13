#!/usr/bin/env python
import datetime
import re

import ev
import settings

from ev import Command as BaseCommand
from ev import default_cmds
from src.utils import create, utils
from game.gamesrc.oasis.lib.oasis import partial_pmatch, send_message, validate_targets, check_ignores
from game.gamesrc.oasis.lib.constants import *
from game.gamesrc.oasis.commands.lineeditor import LineEditor

class Mail(default_cmds.MuxCommand):
    """
Send and receive messages.

To check your messages:
    mail

To check message number 3, type:
    mail 3

To send a message to someone named Thaddius:
    mail Thaddius=Hello there, Thaddius!

To delete message number 4, type:
    mail/delete 4

To delete all of your messages, type:
    mail/delete/all
    """
    key = "mail"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def list_mail(self):
        """
        List mail to the calling user.
        """
        mail = self.caller.db.mail
        MESSAGE = 0
        TIMESTAMP = 1
        READ = 2
        try:
            messages = [item for item in mail if item[TIMESTAMP] <= item[MESSAGE].date_sent]
            # Let's clean up mail storage for this user while we're at it.
            self.caller.db.mail = messages
        except TypeError:
            messages = []
        header = '--------Mailbox for %s' % self.caller.name
        self.caller.msg(header)
        count = 1
        for message in messages:
            if message[READ]:
                read = ''
            else:
                read = '{w*'
            self.caller.msg('%s%s. From %s: %s{n' % (read, count, message[MESSAGE].senders[0], message[MESSAGE].header))
            count += 1
        self.caller.msg('-'*len(header))

    def mail_check(self):
        messages = self.caller.db.mail
        if not messages:
            if not self.args.lower() == 'quiet':
                self.caller.msg(ALERT % "You have no new messages.")
            return
        count = 0
        READ = 2
        for message in messages:
            if not message[READ]:
                count += 1
        if not count and not self.args.lower() == 'quiet':
            self.caller.msg(ALERT % "You have no new messages.")
        else:
            self.caller.msg(ALERT % "You have %s new message(s). Check them with: mail" % count)

    def display_mail(self, message):
        """
        Display a mail message.
        """
        senders = ', '.join([ sender.name for sender in message.senders if utils.inherits_from(sender.typeclass, settings.BASE_CHARACTER_TYPECLASS) ])
        receivers = ', '.join([ receiver.name for receiver in message.receivers if utils.inherits_from(receiver.typeclass, settings.BASE_CHARACTER_TYPECLASS) ])
        self.caller.msg('--------Mail from %s to %s.' % (senders, receivers))
        self.caller.msg('Sent on: %s' % message.date_sent)
        self.caller.msg('Subject: %s\n' % message.header)
        self.caller.msg(message.message)
        self.caller.msg('\nDone.')

    def delete_handler(self):
        """
        Delete a specified message.
        """
        MESSAGE = 0
        TIMESTAMP = 1
        if 'all' in self.switches:
            try:
                messages = [item for item in self.caller.db.mail if item[TIMESTAMP] <= item[MESSAGE].date_sent]
                for message in messages:
                    message[MESSAGE].delete()
            except TypeError, AttributeError:
                pass
            self.caller.db.mail = []
            self.caller.msg(ALERT % "All mail deleted.")
            return
        try:
            choice = int(self.args) - 1
        except ValueError:
            self.caller.msg("'%s' is not a valid message number." % self.args)
            return
        try:
            message = self.caller.mail[choice][MESSAGE]
        except (TypeError, IndexError):
            self.caller.msg("The message number %s does not exist." % self.args)
            return
        self.caller.msg('Deleted message from %s to %s entitled "%s".' % (
            ', '.join([ target.name for target in message.senders if utils.inherits_from(
                target.typeclass, settings.BASE_CHARACTER_TYPECLASS)]),
            ', '.join([ target.name for target in message.receivers if utils.inherits_from(
                target.typeclass, settings.BASE_CHARACTER_TYPECLASS) ]),
            message.header))

        self.caller.mail[choice][MESSAGE].delete()
        del self.caller.db.mail[choice]
        self.caller.save()

    def send_buffer(self, senders, subject, receivers, editor_result):
        """
        This function is called by the line editor when its work is complete.
        """
        # If we're not quitting, we're not doing anything.
        if not editor_result['quitting']:
            self.caller.msg('Saving a draft is not yet supported. Use :wq to send the message.')
            return False
        # If you're typing out a really long mail, you may have annoyed someone in the interim.
        body = editor_result['buffer']
        receivers = check_ignores(self.caller, receivers)
        if not receivers:
            caller.msg('No valid recipients found!')
            return False
        if send_message(senders, subject, body, receivers, send_email=True):
            self.caller.msg('Mail sent.')
            return True
        else:
            self.caller.msg("No messages sent.")
            return False

    def long_handler(self):
        """
        Handles a long form message by calling a line editor.
        """
        receivers = validate_targets(self.caller, self.lhslist, local_only=False)
        if not receivers:
            self.caller.msg('No valid targets found!')
            return
        senders = [self.caller]
        subject = self.rhs
        if not subject:
            self.caller.msg('You must specify a subject. Try: mail/long someone=Hello, there!')
            return

        # The load/save codes define what the editor shall do when wanting to
        # save the result of the editing. This should be a tuple with the first value as a
        # function, and the second value as a dictionary.

        # The save function will have the argument 'editor_result' which will contain a dictionary
        # the line editor sends back. This dictionary will contain 'buffer', the line editor's buffer,
        # and 'caller', the line editor's self.caller.

        # The load function will have the parameters defined by the dictionary in the tuple, as well as
        # an argument 'editor_result', a dictionary which will contain the element 'caller', which holds
        # self.caller.

        # The save function should return a true value if successful, and a false one if it failed.

        loadcode = (lambda **args: '', {}) # Just need an empty string.

        savecode = (self.send_buffer, {'subject': subject, 'senders' : [self.caller], 'receivers' : receivers})

        editor_key = "mail_message"

        # Start the line editor
        LineEditor(self.caller, loadcode=loadcode, savecode=savecode, key=editor_key)

    def main_handler(self):
        """
            Handles arguments if there are no switches. Intended to do the
        'most obvious' action for different arguments.
        """
        MESSAGE = 0
        READ = 2
        if not self.rhs and not self.lhs:
            self.list_mail()
            return
        if self.lhs and not self.rhs:
            try:
                choice = int(self.lhs)
            except ValueError:
                self.caller.msg("'%s' is not a mail message number. Did you mean to send a message to '%s'? If so, try: mail %s=Your message here." % \
                    (self.lhs, self.lhs, self.lhs))
                return
            try:
                # Display numbers are offset.
                message = self.caller.db.mail[choice - 1]
                self.display_mail(message[MESSAGE])
                message[READ] = True
                return
            except (TypeError, IndexError):
                self.caller.msg('No such message number. To check your mail, type: mail')
                return
        if self.rhs and not self.lhs:
            self.caller.msg('You must specify someone to send mail to.')
            return
        receivers = validate_targets(self.caller, self.lhslist, local_only=False)
        if not receivers:
            self.caller.msg('No valid targets found!')
            return
        senders = [self.caller]
        subject = '( Quickmail )'
        body = self.rhs
        if send_message(senders, subject, body, receivers, send_email=True):
            self.caller.msg('Mail sent.')
        else:
            self.caller.msg("No messages sent.")

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the cmdhandler right after self.parser() finishes, and so has access
        to all the variables defined therein.
        """
        self.switches = [ switch.lower() for switch in self.switches ]
        if not self.switches:
            self.main_handler()
            return
        if 'long' in self.switches:
            self.long_handler()
        if 'delete' in self.switches or 'del' in self.switches:
            self.delete_handler()
            return
        if 'check' in self.switches:
            self.mail_check()
