from django import forms


class BackgroundForm(forms.Form):
    """
    Form for setting a user's background.
    """
    # This is about the longest background we've ever received.
    background = forms.CharField(max_length=12000, widget=forms.Textarea)


class DescriptionForm(forms.Form):
    """
    Form for setting a user's description.
    """
    # Descriptions shouldn't be maddeningly long, but should be of good size.
    description = forms.CharField(max_length=6000, widget=forms.Textarea)