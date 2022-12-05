from hotel.models import Hotel, Facility
from django.forms import ModelForm
from django import forms

class HotelForm(ModelForm):
    class Meta:
        model=Hotel
        fields=['name']

class FacilityForm(ModelForm):
    class Meta:
        model=Facility
        fields=['name','description']

