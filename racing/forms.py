from django import forms
from .mock import data_race
from .mock import data_driver
from .mock import data_grid
from .mock import data_constructor
class RacingForm(forms.Form):
    driver = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=data_driver,
    )
    race = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=data_race
    )
    constructor = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=data_constructor,
    )
    grid = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=data_grid,
    )
