from django import forms

class IdolSearchForm(forms.Form):
    your_zodiac = forms.CharField(label="Your zodiac", max_length=20)
    your_height = forms.CharField(label="Your height (in CM)", max_length=20)
    your_birthplace = forms.CharField(label="Your birthplace", max_length=20)