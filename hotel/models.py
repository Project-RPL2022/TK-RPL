from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)


class Facility (models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE)
