from django.urls import path
from .views import *

urlpatterns = [
    path("management/", manage_rooms, name="room-management"),
    ]