from django import forms
from .mock import data
class RacingForm(forms.Form):
    # driver = forms.CharField(label='', max_length=100)
    # race = forms.EmailField(label='', max_length=100)
    # constructor = forms.CharField(label='', max_length=100)
    grid = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=data,
    )
