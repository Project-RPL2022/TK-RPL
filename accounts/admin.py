from django.contrib import admin
from .models import HotelUser
from hotel.models import Hotel
from room.models import Room

# Register your models here.

admin.site.register(HotelUser)
admin.site.register(Hotel)
admin.site.register(Room)
