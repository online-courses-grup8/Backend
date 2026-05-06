from rest_framework import serializers
from courses.models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'photo', 'specialization']

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name.split("/")[-1]
        return None

class InstructorDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = [
            "id", "name", "photo", "specialization",
            "experience", "position",
            "bio_hardskill", "bio_softskill",
            "facebook", "instagram", "linkedin", "twitter"
        ]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name.split("/")[-1]
        return None

