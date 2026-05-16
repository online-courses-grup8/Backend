from django.urls import path
from events.views import EventListView, EventDetailView, EventRegisterView, HomeEventListView

urlpatterns = [
    # GET /api/v1/events/ - tüm etkinlikleri listeler
    path('events/', EventListView.as_view(), name='event-list'),
    # GET /api/v1/events/upcoming/ - ana sayfa icin yaklasan 4 etkinlik
    path('events/upcoming/', HomeEventListView.as_view(), name='upcoming-event-list'),
    # GET /api/v1/events/<slug>/ - etkinlik detayı
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
    # POST /api/v1/events/<slug>/register/ - ticket satın alma
    path('events/<slug:slug>/register/', EventRegisterView.as_view(), name='event-register'),
]