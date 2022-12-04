from django.db import models


class Hotel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)


class Facility (models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE)
