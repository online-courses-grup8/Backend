from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from core.serializers.newsletter import NewsletterSerializer
from core.services.newsletter import subscribe_newsletter


class NewsletterSubscribeView(APIView):
    # POST /api/v1/newsletter/  email kaydeder
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewsletterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscribe_newsletter(serializer.validated_data['email'])
        return Response({
            "status": 201,
            "payload": {"message": "Başarıyla abone oldunuz."},
            "errorMessage": None
        }, status=status.HTTP_201_CREATED)