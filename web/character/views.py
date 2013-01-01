# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from character.forms import NewCharacter
from django.conf import settings
from character.backend import new_player, activate_player
from character.models import TagCategory, Tag

class Generic:
    pass

def new(request):
    """
    Basic Registration
    """
    if request.method == 'POST':
        form  = NewCharacter(request.POST) # A character generation request was submitted.
        if form.is_valid(): # Everything's good to go!
            # We'll process the data here, now that it's been deemed sane.
            data = form.cleaned_data
            new_player(name=data['name'], email=data['email'],
                password=data['password'], context=request)
            return render_to_response(
                'character/new.html',
                {
                    'complete' : True,
                },
                RequestContext(request)
            )
    else:
            form = NewCharacter() # New request. empty form.
    return render_to_response(
        'character/new.html',
        {
            'new_character' : form,
            'complete' : False,
            'aup' : settings.AUP,
        },
        RequestContext(request)
    )

def activate(request, uid, activation_key):
    """
    Account activation
    """
    activated = activate_player(uid, activation_key, request)
    return render_to_response(
        'character/activation.html',
        { 
            'activated' : activated,
        },
        RequestContext(request)
        
    )

def permissions_bundle(request, target):
    """
        Dictionary of permissions values that can be used to determine what a player
    can and can't do through the interface, relative to a target user.
    """
    requester = request.user
    perms = Generic()
    perms.administrator = False # Highest power level
    perms.wizard = False # Most needed tasks
    perms.staff = False # Some helpful tasks
    perms.helpstaff = False # Some helper functions may exist here.
    perms.is_alt = False # If the users are owned by the same activated email, this will become true.
    perms.same_player = False # If the requesting user and the target are the same

    if not target or not request.user:
        return perms
    if request.user == target:
        perms.same_player = True
    try:
        if ( requester.email.lower() == target.email.lower() ) and requester.is_authenticated() and requester.is_active and target.is_active:
            perms.is_alt = True
    except AttributeError:
        pass
    # Other permissions to be put in later.
    if request.user.is_superuser:
        perms.wizard = True
        perms.staff = True
        perms.helpstaff = True
    if request.user.is_staff:
        perms.staff = True
        perms.helpstaff = True
    return perms

def profile(request, username):
    """
    Character profile
    """
    try:
        user = User.objects.get(username__iexact=username)
        character = user.get_profile().character
        tags = character.get_tags()
    except User.DoesNotExist:
        character = None
        user = None
        tags = {}
    perms = permissions_bundle(request, user)
    return render_to_response(
        'character/profile.html',
        {
            'character' : character,
            'perms'     : perms,
            'target'    : user,
            'tags'      : tags,
        },
        RequestContext(request)
    )
