from rest_framework import serializers
from .models import Category, Instructor, InstructorSkill, Course, CourseSection, CourseLesson, Enrollment, LessonProgress, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'photo', 'specialization']


class CourseListSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
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

    def get_student_count(self, obj):
        return obj.enrollments.count()

    def get_lesson_count(self, obj):
        return CourseLesson.objects.filter(section__course=obj).count()