from rest_framework import serializers
from courses.models import Category


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon']

    # Frontend'e sadece icon name dönmesi için
    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.name.split('/')[-1]
        return None
class CategoryWithCourseCountSerializer(serializers.ModelSerializer):
    # kategori listesi sayfası için, kurs sayısıyla
    icon = serializers.SerializerMethodField()
    course_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'course_count']

    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.name.split('/')[-1]
        return None
