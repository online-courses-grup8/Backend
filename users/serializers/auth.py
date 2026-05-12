# users/serializers/auth.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # kayıt formu için gerekli alanlar
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'profile_image']

    def validate_first_name(self, value):
        # boş olamaz
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value.strip()

    def validate_last_name(self, value):
        # boş olamaz
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value.strip()

    def validate_email(self, value):
        # email daha önce kayıtlı mı kontrol et
        if not value.strip():
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email zaten kayıtlı.")
        return value.lower()  # emaili küçük harfe çevir

    def validate(self, attrs):
        # şifreler eşleşiyor mu kontrol et
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs


class LoginSerializer(serializers.Serializer):
    # giriş formu için gerekli alanlar
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)