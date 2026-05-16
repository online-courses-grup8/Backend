# courses/views/category.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from courses.selectors.category import get_categories_with_course_count
from courses.serializers.category import CategoryWithCourseCountSerializer


class CategoryListView(APIView):
    # GET /api/v1/categories/  kategorileri kurs sayısıyla listeler
    permission_classes = [AllowAny]

    def get(self, request):
        categories = get_categories_with_course_count()
        serializer = CategoryWithCourseCountSerializer(categories, many=True)
        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })