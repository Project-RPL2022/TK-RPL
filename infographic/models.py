from django.db import models
from hotel.models import Hotel
from hotel.models import Facility
from django.dispatch import receiver

# Create your models here.
class Infographic(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField()

@receiver(models.signals.post_delete, sender=Infographic)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            instance.image.delete(save=False)
        except Exception:
            pass


@receiver(models.signals.pre_save, sender=Infographic)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk or not instance.image:
        return
    try:
        old_file = Infographic.objects.get(pk=instance.pk).image
    except Infographic.DoesNotExist:
        return False
    if old_file and old_file.url != instance.image.url:
        old_file.delete(save=False)