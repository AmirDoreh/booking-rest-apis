from rest_framework.serializers import ModelSerializer, SerializerMethodField

from cleaners.models import Cleaner


class CleanersListSerailizer(ModelSerializer):
    available = SerializerMethodField()

    class Meta:
        model = Cleaner
        fields = "__all__"

    def get_available(self, obj):
        return obj.available
