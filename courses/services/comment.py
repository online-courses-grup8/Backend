from courses.models import Comment


def create_course_comment(course, user, validated_data):
    # Login kullanıcı varsa name/email backend tarafından user'dan alınır
    if user and user.is_authenticated:
        name = user.get_full_name() or user.username
        email = user.email

        return Comment.objects.create(
            course=course,
            user=user,
            name=name,
            email=email,
            message=validated_data["message"],
            rating=validated_data["rating"],
        )

    # Guest kullanıcı için name/email request body'den alınır
    return Comment.objects.create(
        course=course,
        user=None,
        name=validated_data["name"],
        email=validated_data["email"],
        message=validated_data["message"],
        rating=validated_data["rating"],
    )