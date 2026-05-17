# core/selectors/stats.py
from courses.models import Course
from courses.models.instructor import Instructor
from courses.models.enrollment import Enrollment


def get_site_stats():
    # site istatistiklerini döner
    return {
        "years_of_experience": 25,  # statik değer
        "classes_completed": Course.objects.filter(is_published=True).count(),
        "expert_instructors": Instructor.objects.count(),
        "students_enrolled": Enrollment.objects.values('user').distinct().count(),
    }