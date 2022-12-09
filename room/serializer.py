from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser',
                   'is_staff', 'groups', 'user_permissions']


class HotelUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = HotelUser
        fields = ['guest_status', 'user']


class CheckoutListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = HotelUser
        fields = ['address', 'guest_status', 'user']
