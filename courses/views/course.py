from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from utils.pagination import CustomPageNumberPagination
from courses.serializers import (
    CourseListSerializer,
    CourseOverviewSerializer,
    CourseSectionSerializer,
    InstructorDetailSerializer,
    CommentSerializer,
)
from courses.selectors.course import (
    get_published_courses,
    get_course_overview,
    get_course_curriculum,
    get_course_instructor,
    get_course_reviews,
)


# Course list (grid) endpoint
# Tüm yayınlanmış kursları pagination ile listeler
class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseListSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return get_published_courses()


# Course overview endpoint
# Sayfa ilk açıldığında gelen temel bilgiler (title, description, meta vb.)
class CourseOverviewView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseOverviewSerializer

    def get_object(self):
        return get_course_overview(self.kwargs["slug"])


# Course curriculum endpoint
# Sections ve lessons bilgilerini döner (tab değişince çağrılır)
class CourseCurriculumView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseSectionSerializer

    def get(self, request, *args, **kwargs):
        course = get_course_curriculum(self.kwargs["slug"])

        # Course içindeki tüm section ve lessonları serialize eder
        serializer = self.get_serializer(course.sections.all(), many=True)

        return Response(serializer.data)


# Course instructor endpoint
# Instructor detay bilgilerini döner
class CourseInstructorView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = InstructorDetailSerializer

    def get_object(self):
        course = get_course_instructor(self.kwargs["slug"])
        return course.instructor


# Course reviews endpoint
# Kursa ait yorumları döner
class CourseReviewsView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        course, summary = get_course_reviews(self.kwargs["slug"])

        reviews = self.get_serializer(course.comments.all(), many=True)

        return Response({
            "average_rating": round(summary["average_rating"] or 0, 1),
            "total_reviews": summary["total_reviews"],
            "rating_distribution": {
                "5": summary["five_star"],
                "4": summary["four_star"],
                "3": summary["three_star"],
                "2": summary["two_star"],
                "1": summary["one_star"],
            },
            "reviews": reviews.data
        })