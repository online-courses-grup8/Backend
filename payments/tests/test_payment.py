from django.test import SimpleTestCase
from payments.serializers.payment import CheckoutSerializer


class CheckoutSerializerTest(SimpleTestCase):
    # CheckoutSerializer için birim testler

    # card_last_four Validasyon Testleri

    def test_valid_card_last_four_accepted(self):
        # geçerli 4 haneli rakam kabul edilmeli
        serializer = CheckoutSerializer(data={"card_last_four": "1234"})
        self.assertTrue(serializer.is_valid())

    def test_card_last_four_required(self):
        # alan eksik olduğunda hata vermeli
        serializer = CheckoutSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("card_last_four", serializer.errors)

    def test_card_last_four_comprehensive_validation(self):
        # karakter tipi, uzunluk ve boşluk senaryolarını test eder
        cases = [
            ("12AB", False),  # harf içeremez
            ("12!@", False),  # özel karakter içeremez
            ("123", False),  # çok kısa
            ("12345", False),  # çok uzun
            (" 123", False),  # başında boşluk
            ("1 24", False),  # arada boşluk
            ("-123", False),  # negatif işaret içeremez
            ("0000", True),  # dört sıfır geçerli bir son 4 hanedir
            ("1234", True),  # standart geçerli durum
        ]

        for value, expected in cases:
            with self.subTest(value=value):
                serializer = CheckoutSerializer(data={"card_last_four": value})
                self.assertEqual(
                    serializer.is_valid(),
                    expected,
                    f"'{value}' değeri {'geçerli' if expected else 'geçersiz'} olmalıydı."
                )

    def test_card_last_four_data_type_validation(self):
        # farklı veri tipleriyle gönderilen değerleri test eder
        # integer olarak gönderilse de serializer bunu string gibi işlemeli
        serializer = CheckoutSerializer(data={"card_last_four": 1234})
        self.assertTrue(serializer.is_valid())

    def test_card_last_four_null_value(self):
        # null (none) değer gönderildiğinde hata vermeli
        serializer = CheckoutSerializer(data={"card_last_four": None})
        self.assertFalse(serializer.is_valid())
        self.assertIn("card_last_four", serializer.errors)