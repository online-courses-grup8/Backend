# users/services/profile.py
from django.contrib.auth import get_user_model

User = get_user_model()


def update_user_profile(user, validated_data):
    # gelen alanları kullanıcıya günceller
    for field, value in validated_data.items():
        setattr(user, field, value)
    user.save()
    return user

def change_user_password(user, current_password, new_password):
    # mevcut şifreyi doğrular
    if not user.check_password(current_password):
        return False, "Current password is incorrect."
    # yeni şifreyi hashleyerek kaydeder
    user.set_password(new_password)
    user.save()
    return True, None