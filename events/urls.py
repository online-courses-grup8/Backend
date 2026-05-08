from django.urls import path
from .views import EventListView, EventDetailView

urlpatterns = [
    # GET /api/v1/events/ → tüm etkinlikleri listeler
    path('events/', EventListView.as_view(), name='event-list'),
    # GET /api/v1/events/<slug>/ → etkinlik detayı
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
]