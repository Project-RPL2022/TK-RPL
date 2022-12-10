from django.urls import path
from .views import *


urlpatterns = [
    path("<int:hotelId>", getInfographic),
    path("image/<int:hotelId>", show_infographic),
]