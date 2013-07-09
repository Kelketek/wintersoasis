from django import forms
from bootstrap_toolkit.widgets import BootstrapPasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=BootstrapPasswordInput())
