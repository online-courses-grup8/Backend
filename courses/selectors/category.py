from django.db.models import Count, Q
from courses.models.category import Category


def get_categories_with_course_count():
    # kategorileri yayınlanan kurs sayısıyla birlikte döner
    return Category.objects.annotate(
        course_count=Count('courses', filter=Q(courses__is_published=True))
    )