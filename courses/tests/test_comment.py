from django.test import SimpleTestCase
from unittest.mock import MagicMock
from courses.serializers.comment import CommentSerializer, CommentCreateSerializer


# Comment listeleme serializer'ı için birim testler (DB gerektirmez)
class CommentSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = CommentSerializer()

    # Mock bir Comment nesnesi oluşturur
    def _make_comment(self, user_exists=False, profile_image_path=None):
        comment = MagicMock()
        if not user_exists:
            comment.user = None
        else:
            comment.user = MagicMock()
            comment.user.is_authenticated = True
            if profile_image_path:
                image = MagicMock()
                image.name = profile_image_path
                comment.user.profile_image = image
            else:
                comment.user.profile_image = None
        return comment

    # --- get_photo Testleri ---

    def test_photo_strips_path_correctly(self):
        # Karmaşık yollardan sadece dosya ismini çekebilmeli
        # media/users/2026/avatar.png -> avatar.png
        comment = self._make_comment(user_exists=True, profile_image_path="media/users/2026/avatar.png")
        result = self.serializer.get_photo(comment)
        self.assertEqual(result, "avatar.png")

    def test_photo_defaults_to_anonymous_if_no_image(self):
        # Kullanıcı var ama resmi yoksa fallback görseli dönmeli
        comment = self._make_comment(user_exists=True, profile_image_path=None)
        result = self.serializer.get_photo(comment)
        self.assertEqual(result, "anonymous.jpeg")

    def test_photo_returns_anonymous_for_none_user(self):
        # Kullanıcı objesi None ise (misafir) fallback görseli dönmeli
        comment = self._make_comment(user_exists=False)
        result = self.serializer.get_photo(comment)
        self.assertEqual(result, "anonymous.jpeg")


# Yorum oluşturma serializer'ı için validasyon testleri
class CommentCreateSerializerTest(SimpleTestCase):

    def setUp(self):
        # Geçerli temel veri seti, her testte manipüle edilecek
        self.valid_payload = {
            "message": "Harika bir ders içeriği, çok faydalandım.",
            "rating": 5
        }

    # Mock request context ile serializer örneği döndürür
    def _get_serializer(self, data, is_authenticated=False):
        request = MagicMock()
        request.user.is_authenticated = is_authenticated
        return CommentCreateSerializer(
            data=data,
            context={"request": request}
        )

    # --- Koşullu Validasyon Testleri ---

    def test_guest_user_requires_name(self):
        # Guest kullanıcı name göndermezse hata fırlatmalı
        serializer = self._get_serializer(self.valid_payload, is_authenticated=False)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_guest_user_requires_email(self):
        # Guest kullanıcı email göndermezse hata fırlatmalı
        data = self.valid_payload.copy()
        data["name"] = "Test User"  # name var ama email yok
        serializer = self._get_serializer(data, is_authenticated=False)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_authenticated_user_validation(self):
        # Giriş yapmış kullanıcı ekstra bilgi girmeden yorum yapabilmeli
        serializer = self._get_serializer(self.valid_payload, is_authenticated=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # --- Veri Tipi ve Sınır Değer Testleri ---

    def test_rating_edge_cases(self):
        # Puanlamanın 1-5 aralığını ve veri tipini denetler
        cases = [
            (1, True),      # Minimum sınır
            (5, True),      # Maksimum sınır
            (0, False),     # Geçersiz (alt)
            (6, False),     # Geçersiz (üst)
            ("5", True),    # String sayı (DRF integer'a coerce eder)
            ("beş", False), # Geçersiz tip
            (4.5, False),   # Geçersiz ondalıklı
        ]
        for rating, expected in cases:
            with self.subTest(rating=rating):
                data = self.valid_payload.copy()
                data.update({"name": "X", "email": "x@x.com", "rating": rating})
                serializer = self._get_serializer(data, is_authenticated=False)
                self.assertEqual(serializer.is_valid(), expected)