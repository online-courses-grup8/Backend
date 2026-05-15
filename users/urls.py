# users/urls.py
from django.urls import path
from users.views.auth import RegisterView, LoginView
from users.views.profile import ProfileView, ProfileUpdateView, ChangePasswordView, DeleteAccountView
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

]