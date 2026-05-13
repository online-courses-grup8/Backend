from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from payments.serializers.payment import CheckoutSerializer, PaymentSerializer
from payments.services.payment import process_checkout


class CheckoutView(APIView):
    # POST /api/v1/checkout/ → ödeme işlemini gerçekleştirir
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payment, enrolled_courses = process_checkout(
                user=request.user,
                card_last_four=serializer.validated_data['card_last_four'],
            )
        except ValidationError as e:
            # servis katmanından gelen hataları yakala
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": e.message}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 201,
            "payload": {
                "payment": PaymentSerializer(payment).data,
                "enrolled_courses": enrolled_courses,
            },
            "errorMessage": None
        }, status=status.HTTP_201_CREATED)