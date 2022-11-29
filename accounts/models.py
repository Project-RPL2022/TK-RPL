from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ROLE_CHOICES = (
    ('HOTEL_ADMINISTRATOR','HOTEL_ADMINISTRATOR'),
    ('HOTEL_SUPERVISOR','HOTEL_SUPERVISOR'),
    ('GUEST','GUEST'),
)

class HotelUser(models.Model):
    def __str__(self):
        return self.user.get_username()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30,choices = ROLE_CHOICES)