from rest_framework import generics
from rest_framework.permissions import AllowAny

from utils.pagination import CustomPageNumberPagination
from courses.serializers import CourseListSerializer
from courses.selectors import get_published_courses


class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseListSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return get_published_courses()