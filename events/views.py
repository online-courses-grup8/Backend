from rest_framework import generics
from rest_framework.permissions import AllowAny
from utils.pagination import CustomPageNumberPagination
from events.serializers import EventListSerializer
from events.selectors import get_all_events


class EventListView(generics.ListAPIView):
    # tüm etkinlikleri listeler
    permission_classes = [AllowAny]
    serializer_class = EventListSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return get_all_events()