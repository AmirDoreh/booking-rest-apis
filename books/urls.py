from django.urls import path

from books.views import BookCreateView


urlpatterns = [path("", BookCreateView.as_view(), name="books-create")]
