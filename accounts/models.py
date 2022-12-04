from django.db import models
from django.contrib.auth.models import User
from hotel.models import Hotel

ROLE_CHOICES = (
    ('HOTEL_ADMINISTRATOR', 'HOTEL_ADMINISTRATOR'),
    ('HOTEL_SUPERVISOR', 'HOTEL_SUPERVISOR'),
    ('GUEST', 'GUEST'),
)

GUEST_STATUS = (
    ('CHECK-IN', 'CHECK-IN'),
    ('CHECK-OUT', 'CHECK-OUT'),
)


class HotelUser(models.Model):
    def __str__(self):
        return self.user.get_username()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    address = models.CharField(max_length=255, null=True, blank=True)
    guest_status = models.CharField(
        max_length=30, choices=GUEST_STATUS, default='CHECK-OUT')
    guest_current_stay = models.OneToOneField(
        Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name="hotel_stay")
    works_at = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name="hotel_work")
