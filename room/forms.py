from django import forms
from django.forms import ModelForm
from .models import Room,RoomOrder

class CreateRoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('status',)

class EditRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class BookRoomForm(ModelForm):
    class Meta:
        model =RoomOrder
        fields='__all__'
        