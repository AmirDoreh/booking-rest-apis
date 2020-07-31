from rest_framework.generics import CreateAPIView

from books.serializers import BookCreateSerializer


class BookCreateView(CreateAPIView):
    serializer_class = BookCreateSerializer
