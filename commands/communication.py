"""
This module contains commands that are used for player communication.

"""

import re
from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils

class Say(default_cmds.MuxCommand):
    """
    Usage:
      say <message>

    Talk to those in your current location.

    Use say/help to get extended configuration options.
    """
    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"
    help_category = "General"

    def do_extended_help(self):
        self.caller.msg("""
{c=={gSay extended options{c=={n

    Say/pose etc has several options for configuration. For instance, you can change the verbs of your say statements with:

say/say verb
say/ask verb
say/exclaim verb

So, if you typed:

say/say rumbles

Your statements would look something like:

Tom rumbles, "This or that."

    If you don't supply a verb, any setting you have will be cleared and it will use the default. You can also use an alternative quote mark:

say/quote ~

Will make your statements like:

Tom rumbles, ~This or that.~

{c======================={n
""")

    def pref_setter(self):
        """
	Handles individual preference settings for say.
	"""
        if len(self.switches) > 1:
	    self.caller.msg("One setting at a time, please, or we'll end up confused!")
	    return

	choice = self.switches[0].lower()
        if choice == "help":
            self.do_extended_help()
            return True

	if choice in ["say", "ask", "exclaim", "quote"]:
	    if not self.args.strip():
	        try:
		    del self.say_sets[choice]
		except KeyError:
		    pass
		self.caller.msg("Setting '" + choice + "' cleared!")
	    else:
	        self.say_sets[choice] = self.args
		self.caller.msg("Set '" + choice + "' to '" + self.args + "'.")
	    self.caller.say = self.say_sets
	    return True

    def ooc_preprocess(self):
        """
            Determines whether an 'ooc' command is intended to be a say or a pose, and turns
        it into one of those.
        """
        string_to_check = self.args.strip()
        if not string_to_check:
            self.cmdstring = "say"
            return
        if string_to_check[0] == ":":
            self.cmdstring = "pose"
            self.args = string_to_check[1:]
            return
        split_args = string_to_check.split(" ",1)
        if split_args[0].lower() == "pose":
            self.cmdstring = "pose"
            self.args = split_args[-1]
	    return
        else:
            self.cmdstring = "say"

    def say_format(self, speech):
        """
	Formats a statement that is autoprepended by a delimiter, such as a quote mark.

	Right now, the delimiter is only ". Others will be provided and more will be done.
	"""
	prefs = self.say_sets.get
	verb_map = { "." : prefs("say","says"), "?" : prefs("ask","asks"), "!" : prefs("exclaim","exclaims") }

        delim = prefs("quote", '"')

	# Check for punctuation.
	d = re.escape(delim)
	match = re.match(r'^.*?(' + d + ').*?(!|[.]|[?])(' + d + ')', delim + speech )
	#match = re.match(r'^' + re.escape(delim) + r'(?!' + re.escape(delim) + r')*?(!|[.]|[?])' + re.escape(delim),  delim + speech)
        if not match:
	    verb = verb_map["."]
	else:
	    # The first match is the one that will be right after the verb, so it's the most relevant.
	    # This won't be perfect but it will work for most cases.
	    # Second group should contain the punctuation we want.
	    verb = verb_map[match.groups()[1]]
        self.msg_prefix += '{c%s{n ' + verb + ', ' + delim + '%s{n'
	return self.msg_prefix % ( self.caller.name, speech)

    def pose_format(self, speech):
        """
	Formats an action as a pose.
	"""
	self.msg_prefix += '{c%s{n' % self.caller.name

	if speech[0] not in [ ":", ",", " ", "'", ";" ]:
	    speech = " " + speech
	return self.msg_prefix + speech

    def process_quotes(self, speech, offset = 0):
        """
	    Auto-add a " if the number of "s is not even. If offset is
	specified, it will add that number to the count before determining if another
	quote should be added.
	"""
	delim = self.say_sets.get("quote", '"')
	# Add a leading space to make this regex work right.
	speech = " " + speech
        count = len(re.findall(r'[^\\](' + re.escape(delim) + ')', speech))

        # Remove that leading space and remove backslash escapes.
	speech = speech[1:].replace("\\" + delim, delim)

        if (count + offset) % 2:
	    return speech + delim
	return speech

    def func(self):
        """
        Route the action properly.
	"""
        caller = self.caller

        # Determine if they have a dictionary of say settings.
        try:
            self.caller.say.keys
            self.say_sets = self.caller.say
        except:
            self.say_sets = {}

        if self.switches:
	    if self.pref_setter():
	        return
	
        if self.cmdstring.lower() == "ooc":
            self.ooc_preprocess()
            self.msg_prefix = "{C[OOC] {n"
        else:
            self.msg_prefix = ""

        if not self.args and self.raw:
	    self.args = self.raw

        if not self.args:
            self.caller.msg("What? You need to specify what you want to pose/say.")
            return

        if self.cmdstring.lower() in [ "say", '"', "'", "sing", "ponder", "think" ]:
	    say = True
	    offset = 1
	else:
	    say = False
	    offset = 0

	speech = self.process_quotes(self.args, offset)

        # calling the speech hook on the location
        speech = caller.location.at_say(caller, speech)

        if say:
	    message = self.say_format(speech)
	else:
	    message = self.pose_format(speech)
                           
        # Send the final message to the room.
        caller.location.msg_contents(message)

class Pose(Say):
    """
    pose - strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """

    key = "pose"
    aliases = [':', "emote"]
    locks = "cmd:all()"
    help_category = "General"

class Ooc(Say):
    """
    ooc - Speak or pose with an Out of Character marker.
    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      ooc Hello, there!
       -> others will see:
      (OOC) Tom says, "Hello, there!"
    Example 2:
      ooc :waves.
       -> others will see:
      (OOC) Tom waves.

    Prepend OOC to a pose or statment.
    """
    key = "ooc"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"
