from rest_framework import serializers
from events.models import Event, EventRegistration

class EventListSerializer(serializers.ModelSerializer):
    # event listesi sayfası için
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'date', 'start_time', 'end_time','description']

#event detail
class EventDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'requirements','requirements_list',
            'date', 'start_time', 'end_time',
            'hall_number', 'location', 'latitude', 'longitude',
            'is_online', 'language', 'phone', 'email',
            'image', 'image2', 'image3',
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.name.split("/")[-1]
        return None

    def get_image2(self, obj):
        if obj.image2:
            return obj.image2.name.split("/")[-1]
        return None

    def get_image3(self, obj):
        if obj.image3:
            return obj.image3.name.split("/")[-1]
        return None



class EventRegistrationSerializer(serializers.ModelSerializer):
    # etkinliğe kayıt için
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'registered_at']
        read_only_fields = ['id', 'registered_at']



class HomeEventSerializer(serializers.ModelSerializer):
    # ana sayfa upcoming events için
    image = serializers.SerializerMethodField()
    timeRange = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'image', 'category', 'timeRange']

    def get_image(self, obj):
        if obj.image:
            return obj.image.name.split('/')[-1]
        return None

    def get_timeRange(self, obj):
        start = obj.start_time.strftime('%H:%M')
        end = obj.end_time.strftime('%H:%M')
        return f"{start} - {end}"