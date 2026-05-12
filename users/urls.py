# users/urls.py
from django.urls import path
from users.views.auth import RegisterView, LoginView

urlpatterns = [
    # POST /api/v1/auth/register/
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    # POST /api/v1/auth/login/
    path('auth/login/', LoginView.as_view(), name='auth-login'),
]