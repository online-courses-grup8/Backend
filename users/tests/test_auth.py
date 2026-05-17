"""
Test Case #255 / Task #255 - Registration feature backend test coverage
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/255

Goal:
Verify the backend unit test coverage for the user registration feature,
including serializer validation rules and internal authentication services.

Flow:
1. Validate first name rules for empty, short, numeric, and valid values
2. Validate password complexity rules
3. Validate password and confirm password matching rules
4. Verify the register_user service creates a user in the database
5. Verify generated access and refresh tokens contain the correct user data
6. Verify login_user returns tokens for valid credentials
7. Verify login_user rejects invalid credentials
8. Verify refresh_access_token rejects invalid token scenarios
"""

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from rest_framework import serializers
from users.serializers.auth import RegisterSerializer
from users.services.auth import login_user, refresh_access_token, register_user


User = get_user_model()


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


class AuthServiceTest(TestCase):
    def _valid_user_data(self):
        return {
            "first_name": "Ayse",
            "last_name": "Yilmaz",
            "email": "ayse.yilmaz@example.com",
            "password": "Password1",
            "confirm_password": "Password1",
            "phone_number": "+90 555 123 4567",
        }

    def test_register_user_creates_user_and_returns_valid_tokens(self):
        user, access_token, refresh_token, expires_at = register_user(self._valid_user_data())

        created_user = User.objects.get(email="ayse.yilmaz@example.com")
        access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])

        self.assertEqual(user, created_user)
        self.assertEqual(created_user.username, created_user.email)
        self.assertEqual(created_user.first_name, "Ayse")
        self.assertEqual(created_user.last_name, "Yilmaz")
        self.assertEqual(created_user.phone_number, "+90 555 123 4567")
        self.assertTrue(created_user.check_password("Password1"))
        self.assertEqual(access_payload["type"], "access")
        self.assertEqual(access_payload["user_id"], created_user.id)
        self.assertEqual(access_payload["email"], created_user.email)
        self.assertEqual(refresh_payload["type"], "refresh")
        self.assertEqual(refresh_payload["user_id"], created_user.id)
        self.assertTrue(expires_at)

    def test_login_user_returns_tokens_for_valid_credentials(self):
        User.objects.create_user(
            username="ayse.yilmaz@example.com",
            email="ayse.yilmaz@example.com",
            password="Password1",
        )

        user, access_token, refresh_token, expires_at = login_user(
            email="ayse.yilmaz@example.com",
            password="Password1",
        )

        self.assertEqual(user.email, "ayse.yilmaz@example.com")
        self.assertTrue(access_token)
        self.assertTrue(refresh_token)
        self.assertTrue(expires_at)

    def test_login_user_returns_none_values_for_invalid_credentials(self):
        User.objects.create_user(
            username="ayse.yilmaz@example.com",
            email="ayse.yilmaz@example.com",
            password="Password1",
        )

        user, access_token, refresh_token, expires_at = login_user(
            email="ayse.yilmaz@example.com",
            password="WrongPassword1",
        )

        self.assertIsNone(user)
        self.assertIsNone(access_token)
        self.assertIsNone(refresh_token)
        self.assertIsNone(expires_at)

    def test_refresh_access_token_returns_new_access_token_for_valid_refresh_token(self):
        user, _, refresh_token, _ = register_user(self._valid_user_data())

        access_token, expires_at = refresh_access_token(refresh_token)
        access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

        self.assertEqual(access_payload["type"], "access")
        self.assertEqual(access_payload["user_id"], user.id)
        self.assertEqual(access_payload["email"], user.email)
        self.assertTrue(expires_at)


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
