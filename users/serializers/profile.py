# users/serializers/profile.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    # profil bilgilerini döner
    profile_image = serializers.SerializerMethodField()
    enrollment_count = serializers.IntegerField(read_only=True)  # annotate'den gelir
    payment_count = serializers.IntegerField(read_only=True)  # annotate'den gelir

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email',
            'phone_number', 'profile_image', 'created_at',
            'enrollment_count', 'payment_count'
        ]
        read_only_fields = ['id', 'email', 'created_at']

    def get_profile_image(self, obj):
        # sadece dosya adını döner
        if obj.profile_image:
            return obj.profile_image.name.split("/")[-1]
        return "anonymous.jpeg"

class ProfileUpdateSerializer(serializers.ModelSerializer):
    # profil güncelleme için - sadece değiştirilen alanlar gönderilir
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_image']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'profile_image': {'required': False},
        }

        def validate_first_name(self, value):
            # boş olamaz, sadece harf, max 50 karakter
            if not value.strip():
                raise serializers.ValidationError("First name is required.")
            if len(value.strip()) > 50:
                raise serializers.ValidationError("First name must be at most 50 characters.")
            if not value.strip().isalpha():
                raise serializers.ValidationError("First name must contain only letters.")
            return value.strip()

        def validate_last_name(self, value):
            # boş olamaz, sadece harf, max 50 karakter
            if not value.strip():
                raise serializers.ValidationError("Last name is required.")
            if len(value.strip()) > 50:
                raise serializers.ValidationError("Last name must be at most 50 characters.")
            if not value.strip().isalpha():
                raise serializers.ValidationError("Last name must contain only letters.")
            return value.strip()

        def validate_phone_number(self, value):
            # sadece rakam, +, -, boşluk içerebilir
            if not re.match(r'^[\d\s\+\-]{7,15}$', value):
                raise serializers.ValidationError("Enter a valid phone number.")
            return value

