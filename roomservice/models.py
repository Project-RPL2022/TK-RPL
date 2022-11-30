from django.db import models
from hotel.models import Hotel
from accounts.models import HotelUser

ROOM_SERVICE_STATUS = (
    ('AVAILABLE', 'AVAILABLE'),
    ('UNAVAILABLE', 'UNAVAILABLE'),
)

ROOM_SERVICE_ORDER_STATUS = (
    ('WAITING', 'WAITING'),
    ('PROCESSED', 'PROCESSED'),
    ('REJECTED', 'REJECTED'),
    ('FINISHED', 'FINISHED'),
)

PAYMENT_STATUS = (
    ('WAITING', 'WAITING'),
    ('UNVERIFIED', 'UNVERIFIED'),
    ('VERIFIED', 'VERIFIED'),
)


class RoomService(models.Model):
    type = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30, choices=ROOM_SERVICE_STATUS, default="AVAILABLE")
    price = models.FloatField(default=0)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="room_services")


class RoomServiceOrder(models.Model):
    order_date = models.DateTimeField()
    status = models.CharField(
        max_length=30, choices=ROOM_SERVICE_ORDER_STATUS, default="WAITING")
    room_service = models.ForeignKey(
        RoomService, on_delete=models.SET_NULL, null=True, blank=True, related_name="room_services_orders")
    guest = models.ForeignKey(
        HotelUser, on_delete=models.CASCADE, related_name="room_services_orders")


class RoomServicePayment(models.Model):
    amount = models.FloatField(default=0)
    status = models.CharField(
        max_length=30, choices=PAYMENT_STATUS, default="WAITING")
    room_service_order = models.OneToOneField(
        RoomServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)
