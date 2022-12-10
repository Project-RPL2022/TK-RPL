from django.urls import path
from .views import *


urlpatterns = [
    path("", payment_list),
    path("room_order/<int:room_payment_id>", pay_room_payment),
    path("room_order/detail/<int:room_payment_id>", get_room_payment_detail),
    path("api/room_order/detail/<int:room_payment_id>", get_room_payment_detail_api),
    path("room_service_order/<int:room_service_payment_id>", pay_room_service_payment),
    path("room_service_order/detail/<int:room_service_payment_id>", get_room_service_payment_detail),
    path("api/room_service_order/detail/<int:room_service_payment_id>", get_room_service_payment_detail_api),
    path("verify/", get_payment_info, name="payment-verification"),
    path("verify/<int:room_payment_id>", room_payment_verify),
    path("verify/<int:room_service_payment_id>", room_service_payment_verify),
    path("verify/<int:room_service_payment_id>/reject", room_service_payment_reject),
]