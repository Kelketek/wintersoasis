from Crypto.Random import random
from django.contrib.auth.views import login as authlogin
from django.contrib.auth.views import logout as authlogout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import string

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def login(request, *args, **kwargs):
    response = authlogin(request, *args, **kwargs)
    if request.user.is_authenticated():
        lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(30)]
        key = "".join(lst)
        request.user.db.magic_cookie = key
    return response

def logout(request, *args, **kwargs):
    if request.user.is_authenticated():
        del request.user.db.magic_cookie
    return authlogout(request, *args, **kwargs)

def login_gateway(request):
    context_instance = RequestContext(request)
    login_vars = {}
    login_vars['next'] = request.GET.get('next', default=request.POST.get('next', None))
    return render_to_response('flatpages/login.html', login_vars, context_instance)

def custom_500(request):
    return render_to_response('500.html', {}, RequestContext(request))

def page_index(request):
    """
    Main root page.
    """
    context_instance = RequestContext(request)
    context_instance['rip'] = request.META['REMOTE_ADDR']
    return render_to_response('index.html', context_instance)
