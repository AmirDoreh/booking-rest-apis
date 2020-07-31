from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from cleaners.models import Cleaner


def validate_cleaner(cleaner):
    """Validate cleaner is available"""

    # if cleaner is id
    if type(cleaner) == int:
        cleaner = Cleaner.objects.get(id=cleaner)

    if not cleaner.available:
        raise ValidationError("Cleaner is not availble")


class Book(models.Model):
    CLEAN_CHOICES = (("2H", "2 hours"), ("4H", "4 hours"))

    cleaner = models.ForeignKey(
        Cleaner, on_delete=models.CASCADE, validators=[validate_cleaner]
    )
    clean_duartion = models.CharField(choices=CLEAN_CHOICES, max_length=150)


@receiver(post_save, sender=Book)
def handle_cleaner_time(sender, instance, **kwargs):
    """Sets cleaning start and finish time when booking created"""

    cleaner = Cleaner.objects.get(id=instance.cleaner.id)
    now = timezone.now()
    cleaner.cleaning_start_at = now
    duration = (
        timedelta(hours=2) if instance.clean_duartion == "2H" else timedelta(hours=4)
    )
    cleaner.cleaning_finish_at = now + duration
    cleaner.save()
