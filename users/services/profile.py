# users/services/profile.py
from django.contrib.auth import get_user_model

User = get_user_model()


def update_user_profile(user, validated_data):
    # gelen alanları kullanıcıya günceller
    for field, value in validated_data.items():
        setattr(user, field, value)
    user.save()
    return user