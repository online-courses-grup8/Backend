#QUERY LOGİC bu kısımda olur
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from courses.models import Course, CourseSection, CourseLesson
from django.db.models import Count, Avg, Q

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


# Course overview datasını getirir (header + sağ panel bilgileri)
def get_course_overview(slug):
    return get_object_or_404(
        Course.objects.filter(is_published=True)
        .annotate(
            student_count=Count("enrollments", distinct=True),
            lesson_count=Count("sections__lessons", distinct=True)
        )
        .select_related("category", "instructor"),
        slug=slug
    )


# Course curriculum datasını getirir (sections + lessons)
def get_course_curriculum(slug):
    return get_object_or_404(
        Course.objects.filter(is_published=True)
        .prefetch_related(
            Prefetch(
                "sections",
                queryset=CourseSection.objects.order_by("order").prefetch_related(
                    Prefetch(
                        "lessons",
                        queryset=CourseLesson.objects.order_by("order")
                    )
                )
            )
        ),
        slug=slug
    )


# Course instructor detay bilgisini getirir
def get_course_instructor(slug):
    return get_object_or_404(
        Course.objects.filter(is_published=True)
        .select_related("instructor"),
        slug=slug
    )


# Course yorumlarını ve rating özetini getirir
def get_course_reviews(slug):
    course = get_object_or_404(
        Course.objects.filter(is_published=True)
        .prefetch_related("comments"),
        slug=slug
    )

    summary = course.comments.aggregate(
        average_rating=Avg("rating"),
        total_reviews=Count("id"),
        five_star=Count("id", filter=Q(rating=5)),
        four_star=Count("id", filter=Q(rating=4)),
        three_star=Count("id", filter=Q(rating=3)),
        two_star=Count("id", filter=Q(rating=2)),
        one_star=Count("id", filter=Q(rating=1)),
    )

    return course, summary

