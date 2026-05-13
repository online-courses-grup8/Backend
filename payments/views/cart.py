# payments/views/cart.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from payments.serializers.cart import CartItemSerializer, CartSerializer, AddToCartSerializer, SyncCartSerializer
from payments.selectors.cart import get_cart_items, get_cart_total, get_or_create_cart
from payments.services.cart import add_to_cart, remove_from_cart, sync_cart


class CartView(APIView):
    # GET /api/v1/cart/ → sepeti getirir
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = get_cart_items(request.user)
        total = get_cart_total(request.user)

        return Response({
            "status": 200,
            "payload": {
                "items": CartItemSerializer(items, many=True).data,
                "total": total,
                "item_count": items.count(),
            },
            "errorMessage": None
        })


class CartAddView(APIView):
    # POST /api/v1/cart/add/ → sepete kurs ekler
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            item = add_to_cart(request.user, serializer.validated_data['course_id'])
        except ValidationError as e:
            # servis katmanından gelen hataları yakala
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": e.message}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 201,
            "payload": CartItemSerializer(item).data,
            "errorMessage": None
        }, status=status.HTTP_201_CREATED)


class CartRemoveView(APIView):
    # DELETE /api/v1/cart/remove/<item_id>/ → sepetten kurs kaldırır
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            remove_from_cart(request.user, item_id)
        except ValidationError as e:
            # item bulunamazsa hata dön
            return Response({
                "status": 400,
                "payload": None,
                "errorMessage": {"detail": e.message}
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": 200,
            "payload": {"message": "Course removed from cart."},
            "errorMessage": None
        })


class CartSyncView(APIView):
    # POST /api/v1/cart/sync/ → local storage'dan sepeti senkronize eder
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SyncCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # her kurs için ekleme dener, sonucu gruplar halinde döner
        result = sync_cart(request.user, serializer.validated_data['course_ids'])

        return Response({
            "status": 200,
            "payload": result,
            "errorMessage": None
        })