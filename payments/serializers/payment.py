from rest_framework import serializers
from payments.models import Payment, PaymentItem


class CheckoutSerializer(serializers.Serializer):
    # ödeme isteği için frontend'den card_last_four alır
    card_last_four = serializers.CharField(max_length=4, min_length=4)

    def validate_card_last_four(self, value):
        # sadece rakam içermeli
        if not value.isdigit():
            raise serializers.ValidationError("Card last four must contain only digits.")
        return value


class PaymentItemSerializer(serializers.ModelSerializer):
    # ödeme detayındaki her kurs kalemi
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = PaymentItem
        fields = ['course_title', 'price']


class PaymentSerializer(serializers.ModelSerializer):
    # checkout response için ödeme özeti
    items = PaymentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'transaction_id',
            'amount',
            'card_last_four',
            'status',
            'payment_date',
            'items',
        ]