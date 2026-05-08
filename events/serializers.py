from rest_framework import serializers
from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    # event listesi sayfası için
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'date', 'start_time', 'end_time','description']

