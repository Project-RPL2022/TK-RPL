from django.urls import path
from .views import *

urlpatterns = [
    path("api/roomservice/", RoomServiceView.as_view(), name="room_service"),
    path('api/roomservice/<int:pk>', RoomServiceDetailView.as_view(),
         name="room_service_detail"),
    path("api/roomservice/update",
         RoomServiceUpdateView.as_view(), name="room_service_update"),
    path('api/roomservice/order', RoomServiceOrderView.as_view(),
         name="room_service_order"),
    path('api/roomservice/order/update', RoomServiceOrderUpdateView.as_view(),
         name="room_service_order_update"),
    path('api/roomservice/order/<int:pk>', RoomServiceOrderDetailView.as_view(),
         name="room_service_order_detail"),
    # pages
    path("roomservice/", RoomServicePage.as_view(), name="room_service_page"),
    path("roomservice/add", RoomServiceAddPage.as_view(),
         name="room_service_add_page"),
    path("roomservice/update/<int:pk>", RoomServiceUpdatePage.as_view(),
         name="room_service_update_page"),
    path('roomservice/<int:pk>', RoomServiceDetailPage.as_view(),
         name="room_service_detail_page"),
    path('roomservice/order', RoomServiceOrderPage.as_view(),
         name="room_service_order_page"),
    path('roomservice/order/<int:pk>', RoomServiceOrderDetailPage.as_view(),
         name="room_service_order_detail_page"),
]
