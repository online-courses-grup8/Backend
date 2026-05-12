import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    # Authorization: Bearer <token> header'ından kullanıcıyı doğrular

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token süresi dolmuş.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Geçersiz token.')

        if payload.get('type') != 'access':
            raise AuthenticationFailed('Geçersiz token türü.')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Kullanıcı bulunamadı.')

        return (user, token)