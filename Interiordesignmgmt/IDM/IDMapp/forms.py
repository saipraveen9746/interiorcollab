# forms.py
from django import forms
from .models import OfficeBookDesign

class BookingForm(forms.ModelForm):
    class Meta:
        model = OfficeBookDesign
        fields = ['name', 'email', 'contact_no', 'address']
