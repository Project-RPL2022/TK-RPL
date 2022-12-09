from datetime import datetime
from django.db import models
from hotel.models import Hotel
from accounts.models import HotelUser

ROOM_STATUS = (
    ('AVAILABLE', 'AVAILABLE'),
    ('OCCUPIED', 'OCCUPIED'),
)

ROOM_ORDER_STATUS = (
    ('OCCUPYING', 'OCCUPYING'),
    ('FINISHED', 'FINISHED'),
)

PAYMENT_STATUS = (
    ('WAITING', 'WAITING'),
    ('UNVERIFIED', 'UNVERIFIED'),
    ('VERIFIED', 'VERIFIED'),
)


class Room(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    kapasitas_max = models.IntegerField(default=1)
    price = models.FloatField(default=500)
    tipe = models.CharField(max_length=255)
    status = models.CharField(
        max_length=30, choices=ROOM_STATUS, default="AVAILABLE")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class RoomOrder(models.Model):
    order_date = models.DateTimeField(default=datetime.now())
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=30, choices=ROOM_ORDER_STATUS, default="OCCUPYING")
    guest = models.ForeignKey(
        HotelUser, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True)


class RoomPayment(models.Model):
    price = models.FloatField()
    status = models.CharField(
        max_length=30, choices=PAYMENT_STATUS, default="WAITING")
    room_order = models.OneToOneField(
        RoomOrder, on_delete=models.SET_NULL, null=True, blank=True)


class Checkout(models.Model):
    checkout_date = models.DateTimeField()
    room_order = models.OneToOneField(
        RoomOrder, on_delete=models.SET_NULL, null=True, blank=True)
    verificator = models.ForeignKey(
        HotelUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='verificator_checkout_set')
    guest = models.ForeignKey(
        HotelUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='guest_checkout_set')
