from django.contrib.auth.models import User
from accounts.models import HotelUser


def getHotelUser(username):
    user = User.objects.get(username=username)
    return HotelUser.objects.get(user=user)
