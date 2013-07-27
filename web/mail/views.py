import ujson as json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from forms import ComposeMail
from django.conf import settings
from django.db import transaction
from django.shortcuts import render
from urllib2 import unquote

from src.comms.models import Msg
from lib.mail import get_messages, send_message, Mail, MESSAGE

@login_required
def inbox(request):
   """
       Display character's private messages.
   """
   requester = request.user.db.avatar
   messages = [ Mail(message, requester) for message in get_messages(requester) ]
   status = request.session.get('mail_status', '')
   try:
        del request.session['mail_status']
   except:
        pass
   return render_to_response(
        'mail/inbox.html',
        {  
            'user' : request.user,
            'message_list' : messages,
            'status' : status,
        },
        RequestContext(request)
    )

@login_required
def compose_message(request):
    """
        Compose a mail message.
    """
    if request.method == 'POST': # If the form has been submitted...
        form = ComposeMail(request.user, request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            data = form.cleaned_data
            recipients, status = send_message(request.user.db.avatar, data['subject'], data['message'], data['to'],
                priority=False, send_email=True)
            if recipients:
                prefix = "Message Sent."
            else:
                prefix = "Message sending failed!"
            print status
            request.session['mail_status'] = prefix + '\r\r' + '\r\r'.join(status)
            return HttpResponseRedirect(reverse('mail:inbox'))
    else:
        form = ComposeMail(request.user) # An unbound form

    return render(request, 'mail/compose.html', {
        'form': form,
    })

@login_required
def view_message(request, msg_id):
    READ = 2
    requester = request.user.db.avatar
    try:
        msg_id = int(msg_id)
        messages = get_messages(requester)
        message = [ message for message in messages if message[MESSAGE].id == msg_id ]
        message = message[0]
    except IndexError as e:
        raise Http404
    page = render_to_response(
        'mail/view.html',
        {
            'user' : request.user,
            'message' : Mail(message, requester),
        },
        RequestContext(request)
    )
    message[READ] = True
    requester.db.mail = messages
    return page

@login_required
def delete_message(request):
    """
        Delete a mail message.
    """
    requester = request.user.db.avatar
    post = dict(request.POST)
    if not 'msg_id' in post:
        return HttpResponseBadRequest()
    else:
        try:
            msg_id = int(post['msg_id'][0])
        except:
            return HttpResponseBadRequest()
    try:
        messages = [ message for message in get_messages(requester) if message[MESSAGE].id == msg_id ]
        message = messages[0]
    except IndexError:
        raise Http404
    Mail(message, requester).delete(requester)
    request.session['mail_status'] = 'Message deleted.'
    return HttpResponseRedirect(reverse('mail:inbox'))

