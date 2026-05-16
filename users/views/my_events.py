# users/views/my_events.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.pagination import CustomPageNumberPagination
from users.selectors.my_events import get_my_events
from users.serializers.my_events import MyEventSerializer


class MyEventListView(APIView):
    # GET /api/v1/profile/my-events/ -- kullanıcının kayıtlı etkinliklerini döner
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registrations = get_my_events(request.user)
        paginator = CustomPageNumberPagination()
        result = paginator.paginate_queryset(registrations, request)
        serializer = MyEventSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)