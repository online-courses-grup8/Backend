from rest_framework import serializers
from courses.models import Course
from .category import CategorySerializer
from .instructor import InstructorSerializer


class CourseListSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    instructor = InstructorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'thumbnail',
            'price', 'duration', 'level', 'rating',
            'student_count', 'lesson_count',
            'instructor', 'category'
        ]

    # Frontend'e sadece image name dönmesi için
    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.name.split('/')[-1]
        return None


class CourseOverviewSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    instructor = InstructorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "description", "thumbnail",
            "price", "duration", "level", "language",
            "certification", "rating",
            "student_count", "lesson_count",
            "instructor", "category"
        ]

    # Frontend'e sadece image name dönmesi için
    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.name.split("/")[-1]
        return None