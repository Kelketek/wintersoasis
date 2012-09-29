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
    """
    key = "say"
    aliases = ['"']
    locks = "cmd:all()"
    help_category = "General"

    def say_format(self, speech):
        """
	Formats a statement that is autoprepended by a delimiter, such as a quote mark.

	Right now, the delimiter is only ". Others will be provided and more will be done.
	"""
	return '{c%s{n says, "%s{n' % ( self.caller.name, speech)

    def pose_format(self, speech):
        """
	Formats an action as a pose.
	"""
	pose_prefix = '{c%s{n' % self.caller.name

	if speech[0] not in [ ":", ",", " ", "'" ]:
	    speech = " " + speech
	return pose_prefix + speech

    def process_quotes(self, speech, offset = 0):
        """
	    Auto-add a " if the number of "s is not even. If offset is
	specified, it will add that number to the count before determining if another
	quote should be added.
	"""
	# Add a leading space to make this regex work right.
	speech = " " + speech
        count = len(re.findall(r'[^\\](")', speech))

        # Remove that leading space and remove backslash escapes.
	speech = speech[1:].replace('\\"','"')

        if (count + offset) % 2:
	    return speech + '"'
	return speech

    def func(self):
        """
        Route the action properly.
	"""
        caller = self.caller

        if self.cmdstring.lower() in [ "say", '"', "sing", "ponder", "think" ]:
	    say = True
	    offset = 1
	else:
	    say = False
	    offset = 0

        if not self.args:
	    caller.msg("What? You need to specify what you want to pose/say.")
	    return

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
