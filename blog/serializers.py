from rest_framework import serializers
from blog.models import BlogPost


class BlogListSerializer(serializers.ModelSerializer):
    # liste sayfası için - sadece kart bilgileri
    thumbnail = serializers.SerializerMethodField()
    author_photo = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'thumbnail', 'created_at', 'author_name', 'author_photo', 'author_position']

    def get_thumbnail(self, obj):
        # sadece dosya adını döner
        if obj.thumbnail:
            return obj.thumbnail.name.split("/")[-1]
        return None

    def get_author_photo(self, obj):
        # sadece dosya adını döner
        if obj.author_photo:
            return obj.author_photo.name.split("/")[-1]
        return None


