# forms.py
from django import forms

class CrimeSimilarityForm(forms.Form):
    crime_type = forms.CharField(max_length=100, required=False)
    modus_operandi = forms.CharField(max_length=200, required=False)
    weapon_used = forms.CharField(max_length=100, required=False)
    location = forms.CharField(max_length=100, required=False)
