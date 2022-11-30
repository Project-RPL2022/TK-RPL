from django import forms
from .models import Room
from hotel.models import Hotel

class RoomForm(forms.Form):
    name = forms.CharField(label="name", max_length=255)
    kapasitas_max = forms.IntegerField(label="kapasitas_max")
    tipe = forms.CharField(label="tipe", max_length=255)
    hotel = forms.ModelChoiceField(label="hotel", queryset=Hotel.objects.all().order_by('name'))