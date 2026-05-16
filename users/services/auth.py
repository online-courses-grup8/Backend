# users/services/auth.py
import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone

User = get_user_model()


def generate_tokens(user):
    # kullanıcı için access ve refresh token üretir
    now = timezone.now()
    expires_at = now + datetime.timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME)
    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': expires_at,
        'iat': now,
        'type': 'access',
    }
    refresh_payload = {
        'user_id': user.id,
        'exp': now + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME),
        'iat': now,
        'type': 'refresh',
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token, expires_at.isoformat() 

def register_user(validated_data):
    # yeni kullanıcı oluşturur ve token döner
    validated_data.pop('confirm_password')
    password = validated_data.pop('password')

    user = User(**validated_data)
    user.set_password(password)
    user.username = validated_data['email']
    user.save()

    access_token, refresh_token, expires_at = generate_tokens(user)  # ← expires_at eklendi
    return user, access_token, refresh_token, expires_at


def login_user(email, password):
    # email ve şifre ile kullanıcıyı doğrular
    user = authenticate(username=email, password=password)
    if not user:
        return None, None, None, None

    access_token, refresh_token, expires_at = generate_tokens(user)  # bu kısımda frontende acces token süresi döner
    return user, access_token, refresh_token, expires_at