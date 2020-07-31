from rest_framework.generics import ListAPIView

from cleaners.serializers import CleanersListSerailizer
from cleaners.models import Cleaner


class CleanersListView(ListAPIView):
    serializer_class = CleanersListSerailizer
    queryset = Cleaner.objects.all()
