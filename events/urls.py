from django.urls import path
from .views import EventListView

urlpatterns = [
    # GET /api/v1/events/ → tüm etkinlikleri listeler
    path('events/', EventListView.as_view(), name='event-list'),
]