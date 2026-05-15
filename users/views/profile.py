# users/views/profile.py
# users/views/profile.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.selectors.profile import get_user_profile
from users.serializers.profile import ProfileSerializer, ProfileUpdateSerializer, ChangePasswordSerializer
from users.services.profile import update_user_profile, change_user_password


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

class ChangePasswordView(APIView):
    # PUT /api/v1/profile/change-password/ → şifre değiştirir
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, error = change_user_password(
            user=request.user,
            current_password=serializer.validated_data['current_password'],
            new_password=serializer.validated_data['new_password'],
        )

        if not success:
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": error}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 200,
            "payload": {"message": "Password updated successfully."},
            "errorMessage": None
        })