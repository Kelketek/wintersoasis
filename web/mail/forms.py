import regex
from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.encoding import smart_unicode
from selectable.forms import AutoCompleteWidget
from web.character.lookups import UserLookup

import ev
from src.players.models import PlayerDB

class ComposeMail(forms.Form):
    to = forms.CharField(max_length=256, widget=AutoCompleteWidget(UserLookup, allow_new=True))
    subject = forms.CharField(max_length=150)
    message = forms.CharField(max_length=4000, widget=forms.Textarea)
    send = forms.BooleanField(widget=forms.HiddenInput(attrs={'value':'True'}))

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(ComposeMail, self).__init__(*args, **kwargs)

    def clean_to(self):
        data = self.cleaned_data
        recipients = data.get('to', None)
        targets = []
        MAIN = 0
        if recipients:
            for recipient in [ target.strip() for target in recipients.split(',') ]:
                if not recipient:
                    continue
                try:
                    recipient = ev.search_player(recipient)[MAIN].db.avatar
                except IndexError:
                    raise ValidationError('Player %s does not exist' % recipient)
                if recipient.check_list(self._user, 'ignoring', ignores=False):
                    raise ValidationError('Player %s is ignoring you.' % recipient.name)
                targets.append(recipient)
        else:
            raise ValidationError('You must specify recipients.')
        if not targets:
            raise ValidationError('You must specify recipients.')
        return targets
