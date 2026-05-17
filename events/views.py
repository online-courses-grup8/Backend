from rest_framework import generics
from rest_framework.permissions import AllowAny
from utils.pagination import CustomPageNumberPagination
from events.serializers import EventListSerializer, EventDetailSerializer
from events.selectors import get_all_events, get_event_by_slug
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from events.services import register_for_event
from events.serializers import EventRegistrationSerializer
from events.selectors import get_home_events
from events.serializers import HomeEventSerializer

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


class EventRegisterView(APIView):
    # POST /api/v1/events/<slug>/register/  etkinliğe kayıt olur
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            registration = register_for_event(request.user, slug)
        except ValidationError as e:
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": e.message}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 201,
            "payload": EventRegistrationSerializer(registration).data,
            "errorMessage": None
        }, status=status.HTTP_201_CREATED)



class HomeEventListView(APIView):
    # GET /api/v1/events/upcoming/ - ana sayfa icin yaklasan etkinlikler
    permission_classes = [AllowAny]

    def get(self, request):
        events = get_home_events()
        paginator = CustomPageNumberPagination()
        result = paginator.paginate_queryset(events, request)
        serializer = HomeEventSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)