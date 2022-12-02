from django.contrib import admin
from .models import HotelUser
from hotel.models import Hotel
from room.models import Room
from roomservice.models import RoomService, RoomServiceOrder
from feedback.models import Feedback

# Register your models here.

admin.site.register(HotelUser)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomService)
admin.site.register(RoomServiceOrder)
admin.site.register(Feedback)
