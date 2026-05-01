from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Course
from .serializers import CourseListSerializer


class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]  # login olmadan da görülebilir şimdilik bu şekilde sonra değiştireceğiz
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related(
            'instructor',  # instructor join, ekstra sorgu yapmaz
            'category'     # category join, ekstra sorgu yapmaz
        )