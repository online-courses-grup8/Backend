from rest_framework import generics
from rest_framework.permissions import AllowAny
from utils.pagination import CustomPageNumberPagination
from events.serializers import EventListSerializer, EventDetailSerializer
from events.selectors import get_all_events, get_event_by_slug



class EventListView(generics.ListAPIView):
    # tüm etkinlikleri listeler
    permission_classes = [AllowAny]
    serializer_class = EventListSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return get_all_events()


class EventDetailView(generics.RetrieveAPIView):
    # slug'a göre etkinlik detayını döner
    permission_classes = [AllowAny]
    serializer_class = EventDetailSerializer

    def get_object(self):
        return get_event_by_slug(self.kwargs['slug'])