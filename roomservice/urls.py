from django.urls import path
from .views import *

urlpatterns = [
    path("", RoomServiceView.as_view(), name="room_service"),
    path('<int:pk>', RoomServiceDetailView.as_view(), name="room_service_detail"),
    path('order', RoomServiceOrderView.as_view(), name="room_service_order"),
]
