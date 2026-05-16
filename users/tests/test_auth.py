from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.serializers.auth import RegisterSerializer
from users.services.auth import refresh_access_token


# RegisterSerializer için birim testler
class RegisterSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = RegisterSerializer()

    # validate_first_name Testleri

    def test_first_name_validation(self):
        # çeşitli first_name senaryoları
        cases = [
            ("", True),  # boş string hata fırlatmalı
            ("  ", True),  # sadece boşluk hata fırlatmalı
            ("A", True),  # 1 karakter hata fırlatmalı
            ("A1", True),  # rakam içeren hata fırlatmalı
            ("Ayşe", False),  # geçerli tekli isim
            ("Ayşe Nur", False),  # geçerli iki kelimeli isim
        ]
        for value, should_raise in cases:
            with self.subTest(value=value):
                if should_raise:
                    with self.assertRaises(serializers.ValidationError):
                        self.serializer.validate_first_name(value)
                else:
                    result = self.serializer.validate_first_name(value)
                    self.assertEqual(result, value.strip())

    # validate_password Testleri

    def test_password_complexity(self):
        # karmaşıklık kuralları testi
        cases = [
            ("password1", True),  # büyük harf yok
            ("Password", True),  # rakam yok
            ("Password1", False),  # geçerli şifre
        ]
        for pwd, should_raise in cases:
            with self.subTest(pwd=pwd):
                if should_raise:
                    with self.assertRaises(serializers.ValidationError):
                        self.serializer.validate_password(pwd)
                else:
                    self.assertEqual(self.serializer.validate_password(pwd), pwd)

    # validate (cross-field) Testleri

    def test_passwords_match_logic(self):
        # şifre eşleşme mantığı testi
        # 1. eşleşmeyen şifreler
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate({
                "password": "Password1",
                "confirm_password": "Password2"
            })

        # 2. eşleşen şifreler
        attrs = {"password": "Password1", "confirm_password": "Password1"}
        self.assertEqual(self.serializer.validate(attrs), attrs)


# refresh_access_token service için birim testler
class RefreshAccessTokenTest(SimpleTestCase):

    def test_token_type_and_validity(self):
        # geçersiz veya yanlış tipte token senaryoları
        import jwt
        from django.conf import settings
        from django.utils import timezone

        # 1. tamamen geçersiz string
        with self.assertRaises(ValidationError):
            refresh_access_token("invalid.token.here")

        # 2. yanlış tipte token (access token gönderilmesi)
        payload = {
            'user_id': 1,
            'type': 'access',
            'exp': timezone.now().timestamp() + 3600,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        with self.assertRaises(ValidationError):
            refresh_access_token(token)