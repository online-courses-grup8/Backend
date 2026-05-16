# users/views/my_events.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.selectors.my_events import get_my_events
from users.serializers.my_events import MyEventSerializer


class MyEventListView(APIView):
    # GET /api/v1/profile/my-events/ → kullanıcının kayıtlı etkinliklerini döner
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registrations = get_my_events(request.user)
        serializer = MyEventSerializer(registrations, many=True)
        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })