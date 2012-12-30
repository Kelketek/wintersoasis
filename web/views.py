import datetime
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

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def login_gateway(request):
    context_instance = RequestContext(request)
    login_vars = {}
    login_vars['next'] = request.GET.get('next', default=request.POST.get('next', None))
    return render_to_response('flatpages/login.html', login_vars, context_instance)

def custom_500(request):
    return render_to_response('500.html', {}, RequestContext(request))
