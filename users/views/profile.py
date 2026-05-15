# users/views/profile.py
# users/views/profile.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.selectors.profile import get_user_profile
from users.serializers.profile import ProfileSerializer, ProfileUpdateSerializer
from users.services.profile import update_user_profile


class ProfileView(APIView):
    # GET /api/v1/profile/ → profil bilgilerini döner
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_profile(request.user)
        serializer = ProfileSerializer(user)
        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })


class ProfileUpdateView(APIView):
    # PATCH /api/v1/profile/update/ → profil bilgilerini günceller
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = update_user_profile(request.user, serializer.validated_data)
        updated = get_user_profile(user)

        return Response({
            "status": 200,
            "payload": ProfileSerializer(updated).data,
            "errorMessage": None
        })
class ProfileView(APIView):
    # GET /api/v1/profile/ → profil bilgilerini döner
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_user_profile(request.user)
        serializer = ProfileSerializer(user)
        return Response({
            "status": 200,
            "payload": serializer.data,
            "errorMessage": None
        })

class ProfileUpdateView(APIView):
    # PATCH /api/v1/profile/update/ → profil bilgilerini günceller
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = update_user_profile(request.user, serializer.validated_data)
        updated = get_user_profile(user)

        return Response({
            "status": 200,
            "payload": ProfileSerializer(updated).data,
            "errorMessage": None
        })