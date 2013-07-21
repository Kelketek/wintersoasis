import datetime
from Crypto.Random import random
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login as authlogin
from django.contrib.auth.views import logout as authlogout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.core.urlresolvers import reverse
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
        request.user.get_profile().db.magic_cookie = key
    return response

def logout(request, *args, **kwargs):
    if request.user.is_authenticated():
        del request.user.get_profile().db.magic_cookie
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
    raise Http500
    context_instance = RequestContext(request)
    context_instance['rip'] = request.META['REMOTE_ADDR']
    return render_to_response('index.html', context_instance)
