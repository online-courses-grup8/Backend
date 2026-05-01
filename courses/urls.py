from django.urls import path
from .views import CourseListView

urlpatterns = [
    # GET /api/v1/courses/ → yayındaki kursların listesi
    path('', CourseListView.as_view(), name='course-list'),
]