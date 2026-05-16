from django.urls import path
from .views import (
    CourseListView,
    CourseOverviewView,
    CourseCurriculumView,
    CourseInstructorView,
    CourseReviewsView,
    CourseCommentCreateView,
    InstructorListView,
    InstructorDetailView,
    InstructorOthersView,
    CategoryListView,
    CourseByCategoryView,
)

urlpatterns = [
    # GET /api/v1/courses/
    path('courses/', CourseListView.as_view(), name='course-list'),

    # detail endpoints
    path("courses/<slug:slug>/overview/", CourseOverviewView.as_view(), name="course-overview"),
    path("courses/<slug:slug>/curriculum/", CourseCurriculumView.as_view(), name="course-curriculum"),
    path("courses/<slug:slug>/instructor/", CourseInstructorView.as_view(), name="course-instructor"),
    path("courses/<slug:slug>/reviews/", CourseReviewsView.as_view(), name="course-reviews"),

# POST /api/v1/courses/<slug>/comments/
    path("courses/<slug:slug>/comments/", CourseCommentCreateView.as_view(), name="course-comment-create"),

# instructor endpoint'leri
    path('instructors/', InstructorListView.as_view(), name='instructor-list'),
    path('instructors/<slug:slug>/', InstructorDetailView.as_view(), name='instructor-detail'),
    path('instructors/<slug:slug>/others/', InstructorOthersView.as_view(), name='instructor-others'),
   #Category endpointleri
    # GET /api/v1/categories/
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # GET /api/v1/courses/by-category/ - kategoriye gore kurs listesi
    path('courses/by-category/', CourseByCategoryView.as_view(), name='course-by-category'),
]