from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from cleaners.models import Company, Cleaner
from cleaners.serializers import CleanersListSerailizer


class CleanersTest(TestCase):
    def test_cleaners_list(self):
        google = Company.objects.create(name="google")
        intel = Company.objects.create(name="intel")
        Cleaner.objects.create(company=google)
        Cleaner.objects.create(company=google)
        Cleaner.objects.create(company=intel)
        self.assertEqual(Cleaner.objects.filter(company=google).count(), 2)
        self.assertEqual(Cleaner.objects.filter(company=intel).count(), 1)
        cleaners = Cleaner.objects.all()
        self.assertEqual(cleaners.count(), 3)
        res = self.client.get(reverse("cleaners-list"))
        serializer = CleanersListSerailizer(cleaners, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_cleaners_availablity(self):
        hour = timezone.now().hour
        google = Company.objects.create(name="google")
        cleaner = Cleaner.objects.create(company=google)
        with self.settings(
            CLEANERS_HOLIDAY_WEEKDAY=timezone.now().weekday() + 1,
            CLEANERS_START_WORK_HOUR=hour - 2,
            CLEANERS_END_WORK_HOUR=hour + 12,
        ):
            self.assertTrue(cleaner.available)
            cleaner.cleaning_start_at = timezone.now()
            cleaner.cleaning_finish_at = timezone.now() + timedelta(hours=2)
            self.assertFalse(cleaner.available)

        with self.settings(CLEANERS_HOLIDAY_WEEKDAY=timezone.now().weekday,):
            self.assertFalse(cleaner.available)

        with self.settings(
            CLEANERS_HOLIDAY_WEEKDAY=timezone.now().weekday() + 1,
            CLEANERS_START_WORK_HOUR=hour + 2,
        ):
            self.assertFalse(cleaner.available)
