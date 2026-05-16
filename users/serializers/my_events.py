# users/serializers/my_events.py
from rest_framework import serializers
from events.models import EventRegistration


class EventSummarySerializer(serializers.Serializer):
    # event özet bilgileri
    id = serializers.IntegerField()
    slug = serializers.CharField()
    title = serializers.CharField()
    location = serializers.CharField()
    year = serializers.SerializerMethodField()
    day = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    timeRange = serializers.SerializerMethodField()
    def get_year(self, obj):
        return str(obj.date.year)

    def get_day(self, obj):
        # iki haneli gün
        return str(obj.date.day).zfill(2)

    def get_month(self, obj):
        # ay kısaltması büyük harf
        return obj.date.strftime('%b').upper()

    def get_timeRange(self, obj):
        # başlangıç - bitiş saati formatı
        start = obj.start_time.strftime('%I:%M %p')
        end = obj.end_time.strftime('%I:%M %p')
        return f"{start} - {end}"



class MyEventSerializer(serializers.ModelSerializer):
    # kullanıcının kayıtlı etkinlikleri için
    event = EventSummarySerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'registered_at']