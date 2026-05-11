from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers.contact import ContactMessageSerializer
from core.services.contact import create_contact_message


class ContactMessageCreateView(APIView):
    # POST /api/v1/contact/ → iletişim formunu kaydeder
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_contact_message(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            message=serializer.validated_data['message'],
        )
        return Response(
            {'message': 'Mesajınız alındı, en kısa sürede dönüş yapacağız.'},
            status=status.HTTP_201_CREATED
        )