# users/views/my_courses.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.selectors.my_home import get_recommended_courses
from courses.serializers.course import CourseListSerializer


class RecommendedCoursesView(APIView):
    # GET /api/v1/profile/recommended-courses/ → kategoriye göre önerilen kurslar
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = get_recommended_courses(request.user)
        serializer = CourseListSerializer(courses, many=True)
        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })