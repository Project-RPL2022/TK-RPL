from django.urls import path
from .views import *


urlpatterns = [
    path("room_order/<int:room_payment_id>", pay_room_payment),
    path("room_service_order/<int:room_service_payment_id>", pay_room_service_payment),
]