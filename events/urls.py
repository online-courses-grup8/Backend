from django.urls import path
from .views import EventListView, EventDetailView
from events.views import EventListView, EventDetailView, EventRegisterView

urlpatterns = [
    # GET /api/v1/events/ → tüm etkinlikleri listeler
    path('events/', EventListView.as_view(), name='event-list'),
    # GET /api/v1/events/<slug>/ → etkinlik detayı
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<slug:slug>/register/', EventRegisterView.as_view(), name='event-register'),
]