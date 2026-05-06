from rest_framework import serializers
from courses.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "name", "message", "rating", "created_at"]



class CommentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    message = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, attrs):
        request = self.context.get("request")

        # Login olmayan kullanıcı için name ve email zorunlu
        if not request or not request.user.is_authenticated:
            if not attrs.get("name"):
                raise serializers.ValidationError({"name": "Name is required for guest users."})
            if not attrs.get("email"):
                raise serializers.ValidationError({"email": "Email is required for guest users."})

        return attrs