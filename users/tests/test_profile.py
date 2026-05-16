from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from rest_framework import serializers
from users.serializers.profile import ProfileSerializer, ChangePasswordSerializer
from users.services.profile import change_user_password


# ProfileSerializer için birim testler
class ProfileSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = ProfileSerializer()

    def _make_user(self, image_path=None):
        # mock User objesi oluşturur
        user = MagicMock()
        if image_path:
            image = MagicMock()
            image.name = image_path
            user.profile_image = image
        else:
            user.profile_image = None
        return user

    # get_profile_image Testleri

    def test_profile_image_returns_filename(self):
        # resim varsa derin yollardan bile sadece dosya adını döndürmeli
        cases = [
            ("assets/profile/photo.jpg", "photo.jpg"),
            ("media/users/avatars/2026/test.png", "test.png"),
        ]
        for path, expected in cases:
            with self.subTest(path=path):
                user = self._make_user(image_path=path)
                result = self.serializer.get_profile_image(user)
                self.assertEqual(result, expected)

    def test_profile_image_returns_anonymous_when_missing(self):
        # resim yoksa anonymous.jpeg dönmeli
        user = self._make_user()
        result = self.serializer.get_profile_image(user)
        self.assertEqual(result, "anonymous.jpeg")


# ChangePasswordSerializer için birim testler
class ChangePasswordSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = ChangePasswordSerializer()

    # validate_new_password Testleri

    def test_password_complexity_rules(self):
        # büyük harf, rakam ve özel karakter zorunluluğunu test eder
        cases = [
            ("password1!", True),  # büyük harf yok
            ("Password!", True),  # rakam yok
            ("Password1", True),  # özel karakter yok
            ("Password1!", False),  # geçerli şifre
        ]
        for pwd, should_raise in cases:
            with self.subTest(pwd=pwd):
                if should_raise:
                    with self.assertRaises(serializers.ValidationError):
                        self.serializer.validate_new_password(pwd)
                else:
                    self.assertEqual(self.serializer.validate_new_password(pwd), pwd)

    # validate (cross-field) Testleri

    def test_password_confirmation_match(self):
        # yeni şifreler eşleşmeyince hata fırlatmalı
        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate({
                "new_password": "Password1!",
                "confirm_new_password": "Password2!"
            })

        # eşleşince başarılı dönmeli
        attrs = {"new_password": "Password1!", "confirm_new_password": "Password1!"}
        self.assertEqual(self.serializer.validate(attrs), attrs)


# change_user_password service için birim testler
class ChangeUserPasswordServiceTest(SimpleTestCase):

    def test_password_change_logic_and_side_effects(self):
        # servis katmanının mantığını ve metod çağrılarını test eder
        user = MagicMock()

        # 1. senaryo: mevcut şifre yanlış
        user.check_password.return_value = False
        success, error = change_user_password(user, "wrong", "NewPass1!")
        self.assertFalse(success)
        self.assertEqual(error, "Current password is incorrect.")

        # 2. senaryo: mevcut şifre doğru
        user.check_password.return_value = True
        success, error = change_user_password(user, "correct", "NewPass1!")

        self.assertTrue(success)
        self.assertIsNone(error)
        user.set_password.assert_called_once_with("NewPass1!")
        user.save.assert_called_once()