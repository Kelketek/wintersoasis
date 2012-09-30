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

You can set colors for your quote marks, your text in quote marks, and your text outside of quote marks with:

say/quotecolor color
say/saycolor color
say/posecolor color

The following colors are supported:
{RRed{n, {GGreen{n, {YYellow{n, {BBlue{n, {MMagenta{n,
{CCyan{n, {WWhite{n, and {nNormal, which uses 'uncolored' text.

You can also specify that the color is to be bold. So,
say/saycolor blue
...will make the color {Bblue{n, but
say/saycolor bold blue
...will make the color a {bstrong blue{n.

{c======================={n
""")

    # To get these typles, lowercase a string, split it, and arrange
    # alphabetically before converting.
    COLOR_MAP = {
        ("bold", "red") : "{r",
	("red",) : "{R",
	("bold", "green") : "{g",
	("green",) : "{G",
	("bold", "yellow") : "{y",
	("yellow",) : "{Y",
	("blue", "bold") : "{b",
	("blue",) : "{B",
	("bold", "magenta") : "{m",
	("magenta",) : "{M",
	("bold", "cyan") : "{c",
	("cyan",) : "{C",
	("bold", "white") : "{w",
	("white",) : "{W",
	("normal",) : "{n",
	}


    def determine_color(self, color_string):
        """
	    Get a user's input and check to see if it's in a color map. Return the value
        if so.
	"""
	color  = tuple(sorted(color_string.lower().split()))
	if color in Say.COLOR_MAP:
	    return Say.COLOR_MAP[color]
	return False

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

	if choice in [
	    "say", "ask", "exclaim", "quote",
	    "posecolor", "quotecolor", "saycolor", "namecolor"
	    ]:
	    if not self.args.strip():
	        try:
		    del self.say_sets[choice]
		except KeyError:
		    pass
		self.caller.msg("Setting '" + choice + "' cleared!")
	    else:
	        if choice in ["posecolor", "quotecolor", "saycolor", "namecolor"]:
		    color = self.determine_color(self.args)
		    if color:
		        self.say_sets[choice] = color
			self.caller.msg("Color set for " + color + choice + "{n.")
		    else:
		        self.caller.msg("Couldn't recognize color: " + self.args)
			return True
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

    def statement_type_check(self, speech):
        """
            Determines whether the argument is a declaration, an interrogative,
        or an exclaimatory one.
        """
        prefs = self.say_sets.get
        verb_map = { "." : prefs("say","says"), "?" : prefs("ask","asks"), "!" : prefs("exclaim","exclaims") }

        delim = prefs("quotecolor","{n") + prefs("quote", '"') + "{n"

        # Check for punctuation.
        d = re.escape(delim)
        match = re.match(r'^.*?(' + d + ').*?(!|[.]|[?])(' + d + ')', delim + speech )
        if not match:
            verb = verb_map["."]
        else:
            # The first match is the one that will be right after the verb, so it's the most relevant.
            # This won't be perfect but it will work for most cases.
            # Second group should contain the punctuation we want.
            verb = verb_map[match.groups()[1]]
        return verb

    def say_format(self, speech, speech2=False):
        """
	    Formats one or two strings as a 'say' type statement.
	"""
	prefs = self.say_sets.get
        if speech2:
	    verb = self.statement_type_check(speech2)
            message = self.msg_prefix + speech + prefs("posecolor", "{n") + " " + verb + " " + self.caller.name + ", " + speech2 + '{n'
        else:
	    verb = self.statement_type_check(speech)
            message = self.msg_prefix + self.caller.name + " " + prefs("posecolor", "{n") + verb + ', {n' + speech + '{n' 
	return message

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

	Also, break the text into sections to colorize.
	"""
	prefs = self.say_sets.get
	delim_raw = prefs("quote", '"')
	delim = prefs("quotecolor","{n") + delim_raw + "{n"
	# Add a leading space to make this regex work right.
	speech = " " + speech
        count = len(re.findall(r'[^\\](' + re.escape(delim_raw) + ')', speech))

        # Remove that leading space and remove backslash escapes.
	speech = speech[1:].replace("\\" + delim_raw, delim_raw)

        if (count + offset) % 2:
	    speech = speech + delim_raw

	# How many items we've iterated over.
	raw_count = 0
	# How many times we've started a new colored section
        count = 0
	speech_parts = speech.split(prefs("quote", '"'))
	speech = ""
	# If the previous section ended with a backslash-- that is, is escaped.
	marker = False

	for part in speech_parts:
	    raw_count += 1
	    if marker:
		if part[-1] == '\\':
		    speech += part[:-1]
		    marker = True
		else:
		    speech += part
		    marker = False
		if not raw_count == len(speech_parts):
		    if marker:
		        speech += delim_raw
		    else:
		        speech += delim
		continue
	    if not count % 2:
	        part = prefs("posecolor", "{n") + part
		if part[-1] == '\\':
		    marker = True
		    part = part[:-1]
		else:
		    count += 1
		    marker = False
		    part = part
	    else:
	        part = prefs("saycolor", "{n") + part
		if part[-1] == '\\':
		    marker = True
		    part = part[:-1]
		else:
		    marker = False
		    count += 1
	    if not raw_count == len(speech_parts):
	        if marker:
		    part += delim_raw
		else:
		    part += delim
	    speech += part
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

        prefs = self.say_sets.get

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
	    self.args = prefs("quote", '"') + self.args
	else:
	    say = False

        # ,, can be used to split a statement. For instance:
        # say This is a tough job,,but someone has to do it.
        # will yield:
        # "This is a tough job," says Tom, "but someone has to do it."
        if say and prefs("split", True):
	    match = re.match(r'(.*?)(?!\\),,(.*)', self.args)
            if match:
                speech, speech2 = match.groups()
                speech = speech + ','
		speech = self.process_quotes(speech)
		speech2 = prefs("quote", '"') + speech2
		speech2 = self.process_quotes(speech2)
                message = self.say_format(speech, speech2)
        
	try:
            message
        except UnboundLocalError:
	    speech = self.process_quotes(self.args)
            if say:
                message = self.say_format(speech)
            else:
                message = self.pose_format(speech)

        # calling the speech hook on the location
        caller.location.at_say(caller, message)

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
