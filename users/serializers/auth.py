# users/serializers/auth.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers.fields import Base64ImageField
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # kayıt formu için gerekli alanlar
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    profile_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'profile_image', 'phone_number']

    def validate_first_name(self, value):
        # boş olamaz
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        # en az 2 karakter olmalı
        if len(value.strip()) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters.")
        # sadece harf içermeli
        if not value.strip().replace(" ", "").isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value.strip()

    def validate_last_name(self, value):
        # boş olamaz
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        # en az 2 karakter olmalı
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters.")
        # sadece harf içermeli
        if not value.strip().replace(" ", "").isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value.strip()

    def validate_email(self, value):
        # email daha önce kayıtlı mı kontrol et
        if not value.strip():
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email zaten kayıtlı.")
        return value.lower()  # emaili küçük harfe çevir

    def validate_password(self, value):
        # en az bir büyük harf olmalı
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        # en az bir rakam olmalı
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value
    
    def validate(self, attrs):
        # şifreler eşleşiyor mu kontrol et
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_phone_number(self, value):
        import re
        # boşsa geç
        if not value.strip():
            return value
        # sadece rakam, +, -, boşluk içerebilir, 7-15 karakter
        if not re.match(r'^[\d\s\+\-]{7,17}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value


class LoginSerializer(serializers.Serializer):
    # giriş formu için gerekli alanlar
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)