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
    def __init__(self, *args, **kwargs):
        super(Username, self).__init__(*args, **kwargs)
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

class NewUser(forms.Form):
    name = Username(help_text="You will only want to put the first name of your character here, as this is also the name you will use to sign in. Spaces are not allowed, but underscores and hyphens are fine.")
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False), max_length=80,
        help_text="A good password is best made by creating a nonsense phrase "
            "you can remember. For instance, 'JulesVerneKickedInTheJewels'.")
    password2 = forms.CharField(widget=forms.PasswordInput(
        render_value=False), max_length=80,
        help_text="Type your password one more time to double-check that "
            "you've entered it correctly. If you haven't typed it the same "
            "twice, you may have made a typo in the original!")
    email = forms.EmailField(help_text="Specify your contact email address. "
        "If you have multiple characters, be sure to use the same email "
        "address for all of them. This allows alternate character aware "
        "features to work.")
    email2 = forms.EmailField(help_text="Type your email one more time to "
        "double-check that you've entered it correctly. If you haven't typed "
        "it the same twice, you may have made a typo in the original!")
    captcha = ReCaptchaField(
        attrs={'theme' : 'white'},
        help_text="This last part's just a formality. We want to make sure "
            "you are a human, whether or not your character is. :)")
    aup = forms.BooleanField(
        help_text="I have read and agree to the Acceptable Use Policy.")

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
