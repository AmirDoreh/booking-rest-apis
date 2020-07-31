from django.urls import path

from cleaners.views import CleanersListView


urlpatterns = [path("", CleanersListView.as_view(), name="cleaners-list")]
