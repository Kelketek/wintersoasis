#!/usr/bin/env python
import datetime

import ev
import settings

from ev import Command as BaseCommand
from ev import default_cmds
from src.utils import create, utils
from game.gamesrc.oasis.lib.oasis import partial_pmatch, send_message, validate_targets

class Mail(default_cmds.MuxCommand):
    """
    Send a mail message to another player.
    """
    key = "mail"
    aliases = []
    locks = "pperm(Immortals)"
    help_category = "General"

    def list_mail(self):
        """
        List mail to the calling user.
        """
        mail = self.caller.db.mail
        MESSAGE = 0
        TIMESTAMP = 1
        try:
            messages = [item[MESSAGE] for item in mail if item[TIMESTAMP] <= item[MESSAGE].date_sent ]
        except TypeError:
            messages = []
        header = '--------Mailbox for %s' % self.caller.name
        self.caller.msg(header)
        count = 1
        for message in messages:
            self.caller.msg('%s. From %s: %s' % (count, message.senders[0], message.header))
        self.caller.msg('-'*len(header))

    def display_mail(self, message):
        """
        Display a mail message.
        """
        senders = ', '.join([ sender.name for sender in message.senders if utils.inherits_from(sender, 'src.objects.models.ObjectDB') ])
        receivers = ', '.join([ receiver.name for receiver in message.receivers if utils.inherits_from(receiver, 'src.objects.models.ObjectDB') ])
        self.caller.msg('--------Mail to %s from %s.' % (senders, receivers))
        self.caller.msg('Sent on: %s' % message.date_sent)
        self.caller.msg('Subject: %s\n' % message.header)
        self.caller.msg(message.message)
        self.caller.msg('\nDone.')

    def delete_handler(self):
        """
        Delete a specified message.
        """
        MESSAGE = 0
        try:
            choice = int(self.args) - 1
        except TypeError:
            self.caller.msg("'%s' is not a valid message number.")
            return
        try:
            message = self.caller.mail[choice][MESSAGE]
        except TypeError, IndexError:
            self.caller.msg("The message number %s does not exist." % choice + 1)
            return
        self.caller.msg('Deleted message from %s to %s entitled "%s".' % (', '.join([ target.name for target in message.senders if utils.inherits_from(target, 'src.objects.models.ObjectDB') ]),
            ', '.join([ target.name for target in message.receivers if utils.inherits_from(target, 'src.objects.models.ObjectDB') ]), message.header))
        self.caller.mail[choice][MESSAGE].delete()
        del self.caller.mail[choice]

    def main_handler(self):
        """
            Handles arguments if there are no switches. Intended to do the
        'most obvious' action for different arguments.
        """
        MESSAGE = 0
        if not self.rhs and not self.lhs:
            self.list_mail()
            return
        if self.lhs and not self.rhs:
            try:
                choice = int(self.lhs)
            except TypeError:
                self.caller.msg("'%s' is not a mail message number. Did you mean to send a message to '%s'? If so, try: mail %s=Your message here." % \
                    (self.lhs, self.lhs, self.lhs))
                return
            #try:
                # Display numbers are offset.
            message = self.caller.db.mail[choice - 1]
            self.display_mail(message[MESSAGE])
            return
            #except TypeError, IndexError:
            #    self.caller.msg('No such message number. To check your mail, type: mail')
            #    return
        if self.rhs and not self.lhs:
            self.caller.msg('You must specify someone to send mail to.')
            return
        receivers = validate_targets(self.caller, self.lhslist, local_only=False)
        if not receivers:
            self.caller.msg('No valid targets found!')
            return
        senders = [self.caller]
        subject = 'Message from %s' % self.caller.name
        body = self.rhs
        send_message(senders, subject, body, receivers)
        self.caller.msg('Mail sent.')

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
        if 'delete' in self.switches:
            self.delete_handler() 
