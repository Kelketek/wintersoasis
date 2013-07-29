from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from roster.forms import NewUser
from roster.backend import new_player, activate_player


def new(request):
    """
    Basic Registration
    """
    if request.method == 'POST':
        form = NewUser(request.POST) # A character generation request was submitted.
        if form.is_valid(): # Everything's good to go!
            # We'll process the data here, now that it's been deemed sane.
            data = form.cleaned_data
            new_player(name=data['name'], email=data['email'],
                password=data['password'], request=request)
            return render_to_response(
                'new.html', {
                    'complete' : True},
                RequestContext(request))
    else:
            form = NewUser() # New request. empty form.
    return render_to_response(
        'new.html',{
            'new_character': form,
            'complete': False},
        RequestContext(request))


def activate(request, uid, activation_key):
    """
    Account activation
    """
    activated = activate_player(uid, activation_key, request)
    if activated:
        messages.success(request, "Your account was successfully activated. Now set it up!")
        return redirect("character:profile", username=request.user.username)
    return render_to_response(
        'activation.html', {
            'activated': activated},
        RequestContext(request))
