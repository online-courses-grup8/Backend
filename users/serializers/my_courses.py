# users/serializers/my_courses.py
from rest_framework import serializers
from courses.models import Course, CourseLesson, CourseSection
from courses.models.enrollment import Enrollment
from courses.models.enrollment import LessonProgress
from courses.serializers.instructor import InstructorSerializer
from courses.serializers.category import CategorySerializer


class MyCourseSerializer(serializers.ModelSerializer):
    # annotate'den gelir
    student_count = serializers.IntegerField(read_only=True)
    lesson_count = serializers.IntegerField(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    completion_percentage = serializers.SerializerMethodField()
    title = serializers.CharField(source='course.title')
    slug = serializers.CharField(source='course.slug')
    price = serializers.DecimalField(source='course.price', max_digits=8, decimal_places=2)
    duration = serializers.IntegerField(source='course.duration')
    level = serializers.CharField(source='course.level')
    rating = serializers.FloatField(source='course.rating')

    class Meta:
        model = Enrollment
        fields = [
            'id', 'title', 'slug', 'thumbnail',
            'price', 'duration', 'level', 'rating',
            'student_count', 'lesson_count',
            'instructor', 'category',
            'completion_percentage', 'enrolled_at'
        ]

    def get_thumbnail(self, obj):
        if obj.course.thumbnail:
            return obj.course.thumbnail.name.split('/')[-1]
        return None

    def get_instructor(self, obj):
        return InstructorSerializer(obj.course.instructor).data

    def get_category(self, obj):
        return CategorySerializer(obj.course.category).data

    def get_completion_percentage(self, obj):
        # completion_count annotate'den gelir
        total = obj.lesson_count if hasattr(obj, 'lesson_count') else 0
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            enrollment=obj,
            is_completed=True
        ).count()
        return round((completed / total) * 100)
class MyCourseLessonSerializer(serializers.ModelSerializer):
    # ders listesi için, is_completed bilgisi context'ten gelir
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = CourseLesson
        fields = ['id', 'title', 'duration', 'order', 'video_url', 'is_completed']

    def get_is_completed(self, obj):
        # context'ten tamamlanan ders id'lerini al
        completed_ids = self.context.get('completed_lesson_ids', [])
        return obj.id in completed_ids


class MyCourseSectionSerializer(serializers.ModelSerializer):
    # bölüm listesi için
    lessons = MyCourseLessonSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSection
        fields = ['id', 'title', 'order', 'lessons']