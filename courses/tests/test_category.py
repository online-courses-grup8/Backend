from django.test import SimpleTestCase
from unittest.mock import MagicMock
from courses.serializers.category import CategorySerializer, CategoryWithCourseCountSerializer


class CategorySerializerTest(SimpleTestCase):

    def _make_category(self, icon_path=None):
        # mock Category objesi oluşturur
        category = MagicMock()
        if icon_path:
            icon = MagicMock()
            icon.name = icon_path
            category.icon = icon
        else:
            category.icon = None
        return category

    # --- CategorySerializer Testleri ---

    def test_icon_returns_filename_when_exists(self):
        # icon varsa sadece dosya adını döndürmeli
        # assets/img/icon.png -> icon.png
        category = self._make_category(icon_path="assets/img/icon.png")
        serializer = CategorySerializer()
        result = serializer.get_icon(category)
        self.assertEqual(result, "icon.png")

    def test_icon_returns_none_when_missing(self):
        # icon yoksa None döndürmeli
        category = self._make_category()
        serializer = CategorySerializer()
        result = serializer.get_icon(category)
        self.assertIsNone(result)

    # --- CategoryWithCourseCountSerializer Testleri ---

    def test_icon_returns_filename_when_exists_with_count_serializer(self):
        # CategoryWithCourseCountSerializer'da da icon sadece dosya adını döndürmeli
        category = self._make_category(icon_path="assets/img/icon.png")
        serializer = CategoryWithCourseCountSerializer()
        result = serializer.get_icon(category)
        self.assertEqual(result, "icon.png")

    def test_icon_returns_none_when_missing_with_count_serializer(self):
        # CategoryWithCourseCountSerializer'da icon yoksa None döndürmeli
        category = self._make_category()
        serializer = CategoryWithCourseCountSerializer()
        result = serializer.get_icon(category)
        self.assertIsNone(result)