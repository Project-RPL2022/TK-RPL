from django import forms
from django.forms import ModelForm
from .models import Room

class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('status',)

class EditRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class BookRoomForm(forms.Form):
    end_date=forms.DateField(
        label='Check Out',
        required=True
    ),
    nama_kamar=forms.CharField(
        label='Nama Kamar',
        required=True
    )
    hotel_stay=forms.CharField(
        label="Nama Hotel",
        required=True
    )