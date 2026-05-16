# users/urls.py
from django.urls import path
from users.views.auth import RegisterView, LoginView, RefreshTokenView
from users.views.profile import ProfileView, ProfileUpdateView, ChangePasswordView, DeleteAccountView
from users.views.my_events import MyEventListView
from users.views.my_home import RecommendedCoursesView, MyInstructorsView
from users.views.my_courses import MyCourseListView, MyCourseDetailView, CompleteLessonView

urlpatterns = [
    # POST /api/v1/auth/register/
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    # POST /api/v1/auth/login/
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # PATCH /api/v1/profile/update/
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('profile/my-events/', MyEventListView.as_view(), name='my-events'),
    path('profile/recommended-courses/', RecommendedCoursesView.as_view(), name='recommended-courses'),
    path('profile/my-instructors/', MyInstructorsView.as_view(), name='my-instructors'),
    # POST /api/v1/auth/refresh/  yeni access token üretir
    path('auth/refresh/', RefreshTokenView.as_view(), name='auth-refresh'),
    # GET /api/v1/profile/my-courses/ - satın aldığı kursları listeler
    path('profile/my-courses/', MyCourseListView.as_view(), name='my-courses'),
    # GET /api/v1/profile/my-courses/<slug>/curriculum/ - kursa ait bölüm ve dersler
    path('profile/my-courses/<slug:slug>/curriculum/', MyCourseDetailView.as_view(), name='my-course-curriculum'),
    # POST /api/v1/profile/my-courses/<slug>/lessons/<lesson_id>/complete/ - dersi tamamlar
    path('profile/my-courses/<slug:slug>/lessons/<int:lesson_id>/complete/', CompleteLessonView.as_view(), name='complete-lesson'),

]