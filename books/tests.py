from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from books.models import Book
from cleaners.models import Cleaner, Company


class BookTest(TestCase):
    def test_book_create(self):
        google = Company.objects.create(name="google")
        cleaner = Cleaner.objects.create(company=google)
        payload = {"cleaner": cleaner.id, "clean_duartion": "2H"}
        res = self.client.post(reverse("books-create"), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        obj = Book.objects.filter(cleaner=payload["cleaner"])
        self.assertTrue(obj.exists())

        hour = timezone.now().hour
        with self.settings(
            CLEANERS_HOLIDAY_WEEKDAY=timezone.now().weekday() + 1,
            CLEANERS_START_WORK_HOUR=hour - 2,
            CLEANERS_END_WORK_HOUR=hour + 12,
        ):
            cleaner.refresh_from_db()
            self.assertFalse(cleaner.available)
