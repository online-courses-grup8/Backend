# users/views/my_courses.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.selectors.my_courses import get_my_courses, get_my_course_curriculum, get_lesson
from users.serializers.my_courses import MyCourseSerializer, MyCourseSectionSerializer
from users.services.my_courses import complete_lesson
from utils.pagination import CustomPageNumberPagination

class MyCourseListView(APIView):
    # GET /api/v1/profile/my-courses/ - satın aldığı kursları listeler
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = get_my_courses(request.user)
        paginator = CustomPageNumberPagination()
        result = paginator.paginate_queryset(enrollments, request)
        serializer = MyCourseSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


class MyCourseDetailView(APIView):
    # GET /api/v1/profile/my-courses/<slug>/curriculum/ kursa ait bölüm ve dersler
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        course, completed_lesson_ids = get_my_course_curriculum(request.user, slug)
        sections = MyCourseSectionSerializer(
            course.sections.all(),
            many=True,
            context={'completed_lesson_ids': list(completed_lesson_ids)}
        )
        return Response({
            "status": 200,
            "payload": {
                "title": course.title,
                "description": course.curriculum_description,
                "sections": sections.data
            },
            "errorMessage": None
        })


class CompleteLessonView(APIView):
    # POST /api/v1/profile/my-courses/<slug>/lessons/<lesson_id>/complete/  dersi tamamlar
    permission_classes = [IsAuthenticated]

    def post(self, request, slug, lesson_id):
        enrollment, lesson = get_lesson(request.user, slug, lesson_id)
        complete_lesson(enrollment, lesson)
        return Response({
            "status": 200,
            "payload": {"message": "Ders tamamlandı."},
            "errorMessage": None
        })