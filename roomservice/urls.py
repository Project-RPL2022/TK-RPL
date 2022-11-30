from django.urls import path
from .views import *

urlpatterns = [
    path("", RoomServiceView.as_view(), name="room_service"),
    path('<int:pk>', RoomServiceDetail.as_view()),
]
