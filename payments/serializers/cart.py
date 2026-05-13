# payments/serializers/cart.py
from rest_framework import serializers
from payments.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    # sepetteki her kurs için özet bilgi
    course_id = serializers.IntegerField(source='course.id', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'course_id', 'course_title', 'thumbnail', 'price', 'added_at']

    def get_thumbnail(self, obj):
        # sadece dosya adını döner
        if obj.course.thumbnail:
            return obj.course.thumbnail.name.split("/")[-1]
        return None


class CartSerializer(serializers.Serializer):
    # sepet özeti, items listesi ve toplam tutar
    items = CartItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    item_count = serializers.IntegerField()


class AddToCartSerializer(serializers.Serializer):
    # sepete ekleme isteği için
    course_id = serializers.IntegerField()


class SyncCartSerializer(serializers.Serializer):
    # local storage sync isteği için
    course_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False  # boş liste gönderilemez
    )