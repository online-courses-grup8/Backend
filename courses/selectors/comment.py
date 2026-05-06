from django.shortcuts import get_object_or_404
from courses.models import Course


# Comment oluşturmak için yayınlanmış course bilgisini getirir
def get_course_for_comment(slug):
    return get_object_or_404(
        Course.objects.filter(is_published=True),
        slug=slug
    )