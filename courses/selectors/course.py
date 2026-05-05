#QUERY LOGİC bu kısımda olur
from django.db.models import Count
from courses.models import Course

# - sadece yayınlanan kursları getirir
# - öğrenci ve ders sayısını annotate eder
# - category ve instructor ilişkilerini optimize eder
def get_published_courses():
    return Course.objects.filter(is_published=True).annotate(
        student_count=Count("enrollments", distinct=True),
        lesson_count=Count("sections__lessons", distinct=True)
    ).select_related(
        "category", "instructor"
    ).order_by("-created_at")