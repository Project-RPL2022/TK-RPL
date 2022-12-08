from django.urls import path
from .views import *

urlpatterns = [
    path("api/roomservice/", RoomServiceView.as_view(), name="room_service"),
    path('api/roomservice/<int:pk>', RoomServiceDetailView.as_view(),
         name="room_service_detail"),
    path('api/roomservice/order', RoomServiceOrderView.as_view(),
         name="room_service_order"),
    # pages
    path("roomservice/", RoomServicePage.as_view(), name="room_service_page"),
    path('roomservice/<int:pk>', RoomServiceDetailPage.as_view(),
         name="room_service_detail_page"),
]
