from datetime import datetime
from django.db import models
from accounts.models import HotelUser


class Feedback(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now())
    sender = models.ForeignKey(
        HotelUser, on_delete=models.CASCADE)
