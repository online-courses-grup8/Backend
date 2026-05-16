from rest_framework import serializers
from core.models.newsletter import NewsletterSubscriber


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    def validate_email(self, value):
        # aynı email zaten kayıtlı mı kontrol et
        if NewsletterSubscriber.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email zaten kayıtlı.")
        return value.lower()