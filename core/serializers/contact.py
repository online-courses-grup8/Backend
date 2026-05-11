from rest_framework import serializers
from core.models.contact import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    # iletişim formu için
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        # boş veya sadece boşluk olamaz
        if not value.strip():
            raise serializers.ValidationError("İsim boş olamaz.")
        return value.strip()

    def validate_email(self, value):
        # boş veya sadece boşluk olamaz
        if not value.strip():
            raise serializers.ValidationError("Email boş olamaz.")
        return value.strip()

    def validate_message(self, value):
        # boş veya sadece boşluk olamaz
        if not value.strip():
            raise serializers.ValidationError("Mesaj boş olamaz.")
        return value.strip()