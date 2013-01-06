"""
Forms used for Character manipulation
"""
import regex
from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils.encoding import smart_unicode

class Username(CharField):
    """
    Used for validating usernames.
    """
    def __init__(self):
        super(Username, self).__init__()
        MAX_USERNAME_LENGTH = 16
        self.validators = [validators.MaxLengthValidator(MAX_USERNAME_LENGTH), self.check_no_spaces, self.check_existing]

    def to_python(self, value):
        "Returns a Unicode object."
        if value in validators.EMPTY_VALUES:
            return u''
        name = smart_unicode(value).strip()
        # Force capitalization, dammit.
        name = name[0].upper() + name[1:]
        return name

    def check_no_spaces(self, username):
        """
        Make sure this user name is sane.
        """
        if regex.search('[[:space:]]',username):
            raise ValidationError("You may not have spaces in your username.")

    def check_existing(self, username):
        """
            Verify a username doesn't exist before giving the OK. Not aomic, but
        unlikely to matter.
        """
        try:
            user = User.objects.get(username__iexact=username)
            # If we're here, the user exists!
            raise ValidationError("A character with that name already exists.")
        except User.DoesNotExist:
            pass

class NewCharacter(forms.Form):
    name = Username()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=80)
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=80)
    email = forms.EmailField()
    email2 = forms.EmailField()
    captcha = ReCaptchaField(attrs={'theme' : 'white'})
    aup = forms.BooleanField()

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords did not match.")

        return password2

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if not email2:
            raise forms.ValidationError("You must confirm your email.")
        if email.lower() != email2.lower():
            raise forms.ValidationError("Your emails did not match.")
        return email2
