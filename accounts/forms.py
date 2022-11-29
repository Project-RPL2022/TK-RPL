from django import forms
from django.contrib.auth.models import User
from .models import HotelUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "password",
            ]
