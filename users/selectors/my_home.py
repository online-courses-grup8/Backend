# users/selectors/my_courses.py
from django.db.models import Count
from courses.models import Course
from courses.models.enrollment import Enrollment
from courses.models.instructor import Instructor

def get_user_enrolled_categories(user):
    # kullanıcının kayıtlı olduğu kurs kategorilerini döner
    return Enrollment.objects.filter(user=user).values_list('course__category', flat=True).distinct()


def get_recommended_courses(user, limit=4):
    # kullanıcının kategorilerine göre sahip olmadığı kursları önerir
    enrolled_course_ids = Enrollment.objects.filter(user=user).values_list('course_id', flat=True)
    category_ids = get_user_enrolled_categories(user)

    return Course.objects.filter(
        is_published=True,
        category__in=category_ids,
    ).exclude(
        id__in=enrolled_course_ids  # zaten sahip olduğu kursları çıkar
    ).annotate(
        student_count=Count('enrollments', distinct=True),
        lesson_count=Count('sections__lessons', distinct=True)
    ).select_related('category', 'instructor')[:limit]


def get_my_instructors(user):
    # kullanıcının kayıtlı olduğu kursların instructorlarını döner
    return Instructor.objects.filter(
        courses__enrollments__user=user
    ).distinct()