# users/views/auth.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from users.services.auth import refresh_access_token
from users.serializers.auth import RegisterSerializer, LoginSerializer
from users.services.auth import register_user, login_user


class RegisterView(APIView):
    # POST /api/v1/auth/register/
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, access_token, refresh_token, expires_at = register_user(serializer.validated_data)

        return Response({
            "status": 201,
            "payload": {
                "access": access_token,
                "refresh": refresh_token,
                "expires_at": expires_at,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "profile_image": user.profile_image.name.split("/")[-1] if user.profile_image else "anonymous.jpeg",
                }
            },
            "errorMessage": None
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    # POST /api/v1/auth/login/
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, access_token, refresh_token,expires_at = login_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if not user:
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": "Email veya şifre hatalı."}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 200,
            "payload": {
                "access": access_token,
                "refresh": refresh_token,
                "expires_at": expires_at,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,

                }
            },
            "errorMessage": None
        }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    # POST /api/v1/auth/refresh/ → yeni access token üretir
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": "Refresh token gerekli."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token, expires_at = refresh_access_token(refresh_token)
        except ValidationError as e:
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": e.message}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 200,
            "payload": {
                "access": access_token,
                "expires_at": expires_at,
            },
            "errorMessage": None
        })