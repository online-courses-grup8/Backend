# users/selectors/my_courses.py
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from courses.models import Course, CourseSection, CourseLesson
from courses.models.enrollment import Enrollment, LessonProgress
from django.db.models import Count

def get_my_courses(user):
    # kullanıcının satın aldığı kursları döner
    return Enrollment.objects.filter(user=user).select_related(
        'course__category', 'course__instructor'
    ).annotate(
        student_count=Count('course__enrollments', distinct=True),
        lesson_count=Count('course__sections__lessons', distinct=True)
    )

def get_my_course_curriculum(user, slug):
    # kullanıcının satın aldığı kursa ait curriculum'u döner
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    # tamamlanan ders id'lerini getir
    completed_lesson_ids = LessonProgress.objects.filter(
        enrollment=enrollment,
        is_completed=True
    ).values_list('lesson_id', flat=True)
    return course, completed_lesson_ids


def get_lesson(user, slug, lesson_id):
    # kullanıcının erişebildiği dersi döner
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)
    lesson = get_object_or_404(CourseLesson, id=lesson_id, section__course=course)
    return enrollment, lesson