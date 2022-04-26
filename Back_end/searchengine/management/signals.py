from django.db.models.signals import post_save
from django.dispatch import receiver

from management import models


@receiver(post_save, sender=models.Robots)
def save_robots(sender, instance, created, **kwargs):
    if created:
        models.Robots.objects.exclude(id=instance.id).delete()
