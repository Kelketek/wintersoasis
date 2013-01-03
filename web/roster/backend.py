"""
Backend functions for the character application.
"""
import string
from src.utils.create import create_player
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Crypto.Random import random

# get_template is what we need for loading up the template for parsing.
from django.template.loader import get_template

# Templates in Django need a "Context" to parse with, so we'll borrow this.
# "Context"'s are really nothing more than a generic dict wrapped up in a
# neat little function call.
from django.template import Context

def switch_to(request, target):
    """
    Switch to another user.
    """
    target.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, target)

def activate_player(uid, activation_key, request):
    """
    Activate a player upon receiving a proper activaton key.
    """
    try:
        user = User.objects.get(id = uid)
        if user.is_active:
            # User is already activated.
            return False
        if user.get_profile().db.activation_key == activation_key:
            user.is_active = True
            user.save()
            switch_to(request, user)
            return True
        else:
            print "Else'd!"
            return False
    except User.DoesNotExist:
        print "NonExistant."
        return False

def send_activation_email(character, request):
    """
        Generate an activation key, set it on a player, then have the user
    emailed with the relevant info.
    """
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
    key = "".join(lst)
    character.player.db.activation_key = key
    send_mail(
        "Welcome to %s!" % settings.SERVERNAME,
        get_template('roster/email.txt').render(
            RequestContext(request, {
                'current_server' : request.META['HTTP_HOST'],
                'key' : key,
                'uid' : character.player.dbobj.id
                }
            )
        ),
        settings.SERVER_EMAIL,
        [character.player.user.email]
    )
    

def new_player(name, email, password, context):
    """
    Easier front-end for creating a new player. Also sends reg email.
    """
    character = create_player(name=name, email=email, password=password,
        permissions=settings.PERMISSION_PLAYER_DEFAULT,
        typeclass=settings.BASE_PLAYER_TYPECLASS,
        character_home=settings.CHARACTER_DEFAULT_HOME)
    character.player.user.is_active = False
    character.player.user.save()
    send_activation_email(character, context)
