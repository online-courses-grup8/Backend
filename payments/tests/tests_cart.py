from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from django.core.exceptions import ValidationError
from payments.serializers.cart import CartItemSerializer, AddToCartSerializer, SyncCartSerializer
from payments.services.cart import sync_cart


# CartItemSerializer için birim testler
class CartItemSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = CartItemSerializer()

    # mock CartItem objesi oluşturur
    def _make_cart_item(self, thumbnail_path=None):
        item = MagicMock()
        if thumbnail_path:
            thumbnail = MagicMock()
            thumbnail.name = thumbnail_path
            item.course.thumbnail = thumbnail
        else:
            item.course.thumbnail = None
        return item

    # --- get_thumbnail Testleri ---

    def test_thumbnail_returns_filename_when_exists(self):
        # thumbnail varsa sadece dosya adını döndürmeli
        item = self._make_cart_item(thumbnail_path="assets/img/course.jpg")
        result = self.serializer.get_thumbnail(item)
        self.assertEqual(result, "course.jpg")

    def test_thumbnail_returns_none_when_missing(self):
        # thumbnail yoksa None döndürmeli
        item = self._make_cart_item()
        result = self.serializer.get_thumbnail(item)
        self.assertIsNone(result)


# AddToCartSerializer için birim testler
class AddToCartSerializerTest(SimpleTestCase):

    def test_course_id_required(self):
        # course_id eksik gönderilince hata dönmeli
        serializer = AddToCartSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("course_id", serializer.errors)

    def test_course_id_accepts_integer(self):
        # geçerli integer kabul edilmeli
        serializer = AddToCartSerializer(data={"course_id": 1})
        self.assertTrue(serializer.is_valid())


# SyncCartSerializer için birim testler
class SyncCartSerializerTest(SimpleTestCase):

    def test_empty_list_rejected(self):
        # boş liste reddedilmeli
        serializer = SyncCartSerializer(data={"course_ids": []})
        self.assertFalse(serializer.is_valid())
        self.assertIn("course_ids", serializer.errors)

    def test_valid_integer_list_accepted(self):
        # geçerli integer listesi kabul edilmeli
        serializer = SyncCartSerializer(data={"course_ids": [1, 2, 3]})
        self.assertTrue(serializer.is_valid())


# sync_cart service için birim testler
class SyncCartServiceTest(SimpleTestCase):

    @patch('payments.services.cart.add_to_cart')
    def test_successful_add_goes_to_added_list(self, mock_add):
        # başarılı ekleme added listesine gitmeli
        mock_add.return_value = MagicMock()
        user = MagicMock()
        result = sync_cart(user, [1])
        self.assertIn(1, result["added"])

    @patch('payments.services.cart.add_to_cart')
    def test_already_owned_goes_to_already_owned_list(self, mock_add):
        # zaten satın alınmış kurs already_owned listesine gitmeli
        mock_add.side_effect = ValidationError("You already own this course.")
        user = MagicMock()
        result = sync_cart(user, [1])
        self.assertIn(1, result["already_owned"])

    @patch('payments.services.cart.add_to_cart')
    def test_already_in_cart_goes_to_already_in_cart_list(self, mock_add):
        # zaten sepette olan kurs already_in_cart listesine gitmeli
        mock_add.side_effect = ValidationError("Course is already in your cart.")
        user = MagicMock()
        result = sync_cart(user, [1])
        self.assertIn(1, result["already_in_cart"])