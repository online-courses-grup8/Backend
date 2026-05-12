from rest_framework import serializers
from courses.models import CourseSection, CourseLesson


class CourseLessonSerializer(serializers.ModelSerializer):
    is_preview = serializers.BooleanField(source="is_free", read_only=True)
    class Meta:
        model = CourseLesson
        fields = ["id", "title", "duration", "order", "is_preview"]


class CourseSectionSerializer(serializers.ModelSerializer):
    lessons = CourseLessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSection
        fields = ["id", "title", "order", "lessons"]