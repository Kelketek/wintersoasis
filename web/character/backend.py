"""
Backend functions for the character application.
"""
import string
from src.utils.create import create_player
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from Crypto.Random import random

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
        if user.db.activation_key == activation_key:
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

def send_activation_email(character, context):
    """
        Generate an activation key, set it on a player, then have the user
    emailed with the relevant info.
    """
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
    key = "".join(lst)
    character.player.db.activation_key = key
    send_mail(
    "Character Activation",
    """
Hello there!

    You recently registered an account with Winter's Oasis. In order to use this account, you will need to activate it. You can activate the account by visiting the following URL:

    https://%s%s/%s/%s/

    If you didn't register with Winter's Oasis, you can ignore this email. The account will be deleted within a few days if it is not activated.
""" % (context.META['HTTP_HOST'], reverse('roster.views.activate', args=(character.player.user.id, key))), settings.SERVER_EMAIL,
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
