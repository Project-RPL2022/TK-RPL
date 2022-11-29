from django.db import models
from hotel.models import Hotel
from accounts.models import HotelUser

ROOM_SERVICE_STATUS = (
    ('AVAILABLE', 'AVAILABLE'),
    ('UNAVAILABLE', 'UNAVAILABLE'),
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
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class RoomServiceOrder(models.Model):
    order_date = models.DateTimeField()
    room_service = models.ForeignKey(
        RoomService, on_delete=models.SET_NULL, null=True, blank=True)
    guest = models.ForeignKey(HotelUser, on_delete=models.CASCADE)


class RoomServicePayment(models.Model):
    price = models.FloatField()
    status = models.CharField(
        max_length=30, choices=PAYMENT_STATUS, default="WAITING")
    room_service_order = models.OneToOneField(
        RoomServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)
