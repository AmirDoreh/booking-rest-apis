from django.db import models
from django.utils import timezone
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Cleaner(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="cleaners"
    )
    cleaning_start_at = models.DateTimeField(null=True, blank=True)
    cleaning_finish_at = models.DateTimeField(null=True, blank=True)

    def _is_work_time(self):
        """Check if is not holiday or is work time"""

        now = timezone.now()

        if (
            now.weekday() == settings.CLEANERS_HOLIDAY_WEEKDAY
            or not settings.CLEANERS_START_WORK_HOUR
            < now.hour
            < settings.CLEANERS_END_WORK_HOUR
        ):
            return False

        return True

    @property
    def available(self):
        if not self._is_work_time():
            return False

        if self.cleaning_finish_at and self.cleaning_finish_at > timezone.now():
            return False

        return True
