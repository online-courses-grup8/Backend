from rest_framework import generics
from rest_framework.permissions import AllowAny
from courses.serializers.instructor import InstructorListSerializer, TeacherDetailSerializer
from courses.selectors.instructor import get_all_instructors, get_instructor_by_slug


class InstructorListView(generics.ListAPIView):
    # tüm eğitmenleri listeler
    permission_classes = [AllowAny]
    serializer_class = InstructorListSerializer

    def get_queryset(self):
        return get_all_instructors()


class InstructorDetailView(generics.RetrieveAPIView):
    # slug'a göre eğitmen detayını döner
    permission_classes = [AllowAny]
    serializer_class = TeacherDetailSerializer

    def get_object(self):
        return get_instructor_by_slug(self.kwargs['slug'])