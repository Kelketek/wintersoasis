#!/usr/bin/env python
import ev
import src.objects.models as models
from settings import SERVERNAME

# DBREF of the OOC meeting place used for the nexus command.
NEXUS = "#2"

# DBREF of the first IC room people warp into.
IC_START = "#2"

# Format of alert messages for use with %.
ALERT = "{g[{y!{g] {c%s{n"

# How many messages a user may have in their mailbox at once. If set to 0, there is no limit.
MAX_MESSAGES = 30

# Email on or off?
EMAIL = False

# Hostname for SMTP server
SMTP_HOST = 'localhost'

# Email address to send from.
MAIL_FROM = 'messages@localhost.local'

# The following two strings are templates for game email messages. The first is for HTML messages.
# The second is for the text version of those messages, for clients which don't support HTML.
# ${from} contains a comma separated list of senders (usually, it's just one sender)
# ${recipients} contains a comma separated list of recipients.
# ${message} contains the mail message sent by the user.

HTML_TEMPLATE = """
<html>
<body>
You have a new message from <strong>${from}</strong> to <strong>${recipients}</strong>:<br />

<p>${message}</p>

To manage your in-game messages, log in to %s.
</body>
</html>
""" % SERVERNAME

TEXT_TEMPLATE = """
You have a new message from ${from} to ${recipients}:

${message}

To check and manage your in-game messages, log in to %s.
""" % SERVERNAME

