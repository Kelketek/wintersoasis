# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from character.forms import NewCharacter
from django.conf import settings
from character.backend import new_player, activate_player

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
        }, RequestContext(request)
    )

def activate(request, uid, activation_key):
    """
    Account activation
    """
    activated = activate_player(uid, activation_key, request)
    print activated
    return render_to_response(
        'character/activation.html',
        { 
            'activated' : activated,
        }, RequestContext(request)
        
    )
