from django.urls import path
from .views import *

urlpatterns = [
    path("management/", manage_rooms, name="room-management"),
    path("management/create/", create_room, name="room-create"),
    path("management/edit/", edit_room, name="room-edit"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
    path("book_room/<str:hotel_name>/<str:room_name>",book_room, name="book_room"),
    path("list_room/<str:hotel_name>",list_room, name="list_room")
]
