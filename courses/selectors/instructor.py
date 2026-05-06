from django.shortcuts import get_object_or_404
from courses.models import Instructor


def get_all_instructors():
    # tüm eğitmenleri listeler
    return Instructor.objects.prefetch_related('skills').all()


def get_instructor_by_slug(slug):
    # slug'a göre eğitmen getirir, yoksa 404 döner
    return get_object_or_404(
        Instructor.objects.prefetch_related('skills'),
        slug=slug
    )