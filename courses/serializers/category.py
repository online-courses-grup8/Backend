from rest_framework import serializers
from courses.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']

        # Frontend'e sadece icon name dönmesi için
        def get_icon(self, obj):
            if obj.icon:
                return obj.icon.name.split('/')[-1]
            return None