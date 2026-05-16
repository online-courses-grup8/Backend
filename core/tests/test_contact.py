from django.test import SimpleTestCase
from core.serializers.contact import ContactMessageSerializer


class ContactMessageSerializerTest(SimpleTestCase):

    def setUp(self):
        # Her test için temiz başlangıç verisi
        self.base_data = {
            "name": "Ayşe Yılmaz",
            "email": "ayse@example.com",
            "message": "Bu mesaj en az on karakter olmalıdır."
        }

    # --- 1. Validasyon Pipeline Testleri ---

    def test_serializer_with_valid_data(self):
        """Geçerli veriyle serializer'ın sorunsuz çalıştığını doğrular."""
        serializer = ContactMessageSerializer(data=self.base_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

    def test_required_fields(self):
        """Zorunlu alanlar eksik gönderildiğinde hata dönmeli."""
        fields = ["name", "email", "message"]

        for field in fields:
            with self.subTest(field=field):
                data = self.base_data.copy()
                data.pop(field)

                serializer = ContactMessageSerializer(data=data)

                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)

    # --- 2. Min Length Testleri ---

    def test_min_length_validation(self):
        """Serializer/model min_length validasyonlarını doğrular."""
        test_cases = [
            ("name", "A", False),
            ("name", "An", True),
            ("message", "123456789", False),
            ("message", "1234567890", True),
        ]

        for field, value, expected_valid in test_cases:
            with self.subTest(field=field, value=value):
                data = self.base_data.copy()
                data[field] = value

                serializer = ContactMessageSerializer(data=data)

                self.assertEqual(serializer.is_valid(), expected_valid)

                if not expected_valid:
                    self.assertIn(field, serializer.errors)

    # --- 3. Email Format Testleri ---

    def test_email_format_validation(self):
        """Geçersiz email formatlarının reddedildiğini doğrular."""
        invalid_emails = [
            "yanlis-mail",
            "ayse@",
            "@domain.com",
            "ayse@.com",
            "ayse.com",
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                data = self.base_data.copy()
                data["email"] = email

                serializer = ContactMessageSerializer(data=data)

                self.assertFalse(serializer.is_valid())
                self.assertIn("email", serializer.errors)

    # --- 4. Whitespace Stripping Testleri ---

    def test_whitespace_stripping(self):
        """Baş ve sondaki boşlukların temizlendiğini doğrular."""
        data = {
            "name": "  Ayşe Yılmaz  ",
            "email": "  ayse@example.com  \n",
            "message": "\t Bu mesaj içeriği boşluklu geliyor. \t"
        }

        serializer = ContactMessageSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        self.assertEqual(
            serializer.validated_data["name"],
            "Ayşe Yılmaz"
        )

        self.assertEqual(
            serializer.validated_data["email"],
            "ayse@example.com"
        )

        self.assertEqual(
            serializer.validated_data["message"],
            "Bu mesaj içeriği boşluklu geliyor."
        )

    # --- 5. Sadece Boşluk Girilmesi Testleri ---

    def test_reject_only_whitespace_inputs(self):
        """Sadece boşluk içeren girdilerin reddedildiğini doğrular."""
        fields = ["name", "email", "message"]

        for field in fields:
            with self.subTest(field=field):
                data = self.base_data.copy()
                data[field] = "     "

                serializer = ContactMessageSerializer(data=data)

                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)