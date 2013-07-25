import ujson as json
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core.cache import get_cache
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mail.forms import ComposeMail

from character.models import TagCategory, Tag
from lib.mail import get_messages, send_message, Mail, MESSAGE

User = get_user_model()

cache = get_cache('default')

class Generic:
    def __str__(self):
        return str(self.__dict__)

def is_alt(request, target):
    """
    Determines if a user is another user's alt.
    """
    try:
        return request.user.db.avatar in target.db.avatar.get_alts()
    except:
        return False

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
    perms.me = False # If either is_alt or same_player is true.

    if not target or not requester.is_authenticated:
        return perms
    if requester == target:
        perms.same_player = True
    perms.is_alt = is_alt(request, target)
    if perms.same_player or perms.is_alt:
        perms.me = True

    # Other permissions to be put in later.
    if requester.is_superuser:
        perms.wizard = True
        perms.staff = True
        perms.helpstaff = True
    if requester.is_staff:
        perms.staff = True
        perms.helpstaff = True
    return perms

def switch(request):
    """
        Allows one to switch to another user. Optionally logs in, if the user
    is an alt of the other user.
    """
    if not request.method == 'POST' or not request.user.is_authenticated:
        raise Http404
    post = dict(request.POST)
    try:
        MAIN = 0
        user = User.objects.get(username__iexact=post['target'][MAIN])
    except (User.DoesNotExist, KeyError):
        # Bogus entry, go back to user's page.
        user = request.user
    do_login = post.get('login', False)
    if is_alt(request, user) and do_login:
        user.backend = 'django.contrib.auth.backends.ModelBackend' 
        login(request, user)
    next_page = user.db.avatar.get_absolute_url()
    return HttpResponseRedirect(next_page)

def profile(request, username):
    """
    Character profile
    """
    try:
        user = User.objects.get(username__iexact=username)
        character = user.db.avatar
        tags = character.get_tags()
    except User.DoesNotExist:
        character = None
        user = None
        tags = {}
    perms = permissions_bundle(request, user)
    return render_to_response(
        'profile.html',
        {
            'character' : character,
            'perms'     : perms,
            'target'    : user,
            'tags'      : tags,
            'request'   : request,
        },
        RequestContext(request)
    )

def ajax_render(original_function):
    """
        Decorator for Ajaxy functions.
    """
    def ajaxize(request):
        get_dict = request.GET.copy()
        try:
            json_dict = json.loads(request.POST['argv'])
        except KeyError:
            json_dict = {}
        json_dict.update(get_dict)
        result = original_function(request, kwargs=json_dict)
        try:
            response = HttpResponse(json.dumps(original_function(request, **json_dict)))
        except TypeError:
            return result
        response['Content-Type'] = 'application/json'
        return response
    return ajaxize

@ajax_render
def character_lookup(request, **kwargs):
    """
        None of the other Ajax goodies did quite what I wanted here, so I'm
    rolling my own for this task.
    """
    MAIN = 0
    try:
        suggestions = [ user.username for user in User.objects.filter(username__istartswith=kwargs['query'][MAIN]) ]
    except KeyError:
        return HttpResponseBadRequest()
    return { 'query' : kwargs['query'][MAIN], 'suggestions' : suggestions }
