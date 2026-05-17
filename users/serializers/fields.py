# users/serializers/fields.py
import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    # Base64 string'i decode edip Django ImageField'ına uygun hale getirir
    # Hem register hem de profile update'de kullanılır

    def to_internal_value(self, data):
        if isinstance(data, str) and 'base64,' in data:
            try:
                # data:image/jpeg;base64,... formatını ayıkla
                format, imgstr = data.split('base64,')
                ext = format.split('/')[-1].split(';')[0]  # jpeg, png, webp vs.
                decoded = base64.b64decode(imgstr)

                # serializer'ın initial_data'sından kullanıcı adını al
                initial_data = getattr(self.parent, 'initial_data', {})
                first_name = initial_data.get('first_name', 'user').strip().replace(' ', '_').lower()
                last_name = initial_data.get('last_name', 'user').strip().replace(' ', '_').lower()
                filename = f"{first_name}_{last_name}.{ext}"

                data = ContentFile(decoded, name=filename)
            except Exception:
                raise serializers.ValidationError("Invalid image format.")
        return super().to_internal_value(data)