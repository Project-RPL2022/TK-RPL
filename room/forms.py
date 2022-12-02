from django import forms
from hotel.models import Hotel

class CreateRoomForm(forms.Form):
    name=forms.CharField(
        label='Nama Kamar',
        required=True,
        max_length=225
    )
    kapasitas_max=forms.IntegerField(
        label="Kapasitas Kamar",
        required=True
    )
    tipe=forms.CharField(
        label="Tipe",
        required=True
    )