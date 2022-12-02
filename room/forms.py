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