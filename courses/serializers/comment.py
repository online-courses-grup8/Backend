from rest_framework import serializers
from courses.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()  # kullanıcı fotoğrafı

    class Meta:
        model = Comment
        fields = ["id", "name", "photo", "message", "rating", "created_at"]

    def get_photo(self, obj):
        # login kullanıcının profil fotoğrafını döndürür
        # guest ise default anonim fotoğraf döner
        if obj.user and obj.user.profile_image:
            return obj.user.profile_image.name.split("/")[-1]
        return "anonymous.jpeg"


class CommentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    message = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            if not attrs.get("name"):
                raise serializers.ValidationError({"name": "Name is required for guest users."})
            if not attrs.get("email"):
                raise serializers.ValidationError({"email": "Email is required for guest users."})

        return attrs