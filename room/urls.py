from django.urls import path
from .views import *

urlpatterns = [
    path("management/", manage_rooms, name="room-management"),
    path("management/create/", create_room, name="room-create"),
    path("management/edit/", edit_room, name="room-edit"),
    path("checkout", CheckoutView.as_view(), name="checkout"),
]
