from django.test import SimpleTestCase
from unittest.mock import patch
from core.serializers.newsletter import NewsletterSerializer


class NewsletterSerializerTest(SimpleTestCase):

    def setUp(self):
        self.filter_patch_path = (
            "core.serializers.newsletter."
            "NewsletterSubscriber.objects.filter"
        )

    # 1. Email Validasyon Testleri

    def test_valid_email_accepted(self):
        # Geçerli email kabul edilmeli.
        with patch(self.filter_patch_path) as mock_filter:
            mock_filter.return_value.exists.return_value = False

            serializer = NewsletterSerializer(data={
                "email": "test@example.com"
            })

            self.assertTrue(serializer.is_valid())
            self.assertEqual(serializer.errors, {})
            self.assertEqual(
                serializer.validated_data["email"],
                "test@example.com"
            )

    def test_invalid_email_rejected(self):
        # Geçersiz email formatları reddedilmeli.
        invalid_emails = [
            "yanlis-mail",
            "ayse@",
            "@domain.com",
            "ayse.com",
            "ayse@.com",
            " ",
            "",
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                with patch(self.filter_patch_path) as mock_filter:
                    mock_filter.return_value.exists.return_value = False
                    serializer = NewsletterSerializer(data={"email": email})
                    self.assertFalse(serializer.is_valid())
                    self.assertIn("email", serializer.errors)

    # 2. Email Dönüştürme Testleri

    def test_email_converted_to_lowercase_and_stripped(self):
        # Email küçük harfe çevrilmeli ve boşluklar temizlenmeli.
        with patch(self.filter_patch_path) as mock_filter:
            mock_filter.return_value.exists.return_value = False

            serializer = NewsletterSerializer(data={
                "email": "  TEST@Example.COM  "
            })

            self.assertTrue(serializer.is_valid())
            self.assertEqual(
                serializer.validated_data["email"],
                "test@example.com"
            )

    # 3. Duplicate Email Testleri

    def test_duplicate_email_rejected(self):
        # Zaten kayıtlı email reddedilmeli.
        with patch(self.filter_patch_path) as mock_filter:
            mock_filter.return_value.exists.return_value = True

            serializer = NewsletterSerializer(data={
                "email": "existing@example.com"
            })

            self.assertFalse(serializer.is_valid())
            self.assertIn("email", serializer.errors)

    def test_duplicate_email_check_uses_normalized_email(self):
        # Duplicate kontrolü normalize edilmiş email ile yapılmalı.
        with patch(self.filter_patch_path) as mock_filter:
            mock_filter.return_value.exists.return_value = True

            serializer = NewsletterSerializer(data={
                "email": "  EXISTING@Example.COM  "
            })

            self.assertFalse(serializer.is_valid())
            self.assertIn("email", serializer.errors)