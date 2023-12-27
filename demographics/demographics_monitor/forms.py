from django import forms
import datetime


def year_choices():
    return [(r, r) for r in range(datetime.date.today().year-1, 2009, -1)]


class UserForms(forms.Form):
    year = forms.ChoiceField(choices=year_choices)
