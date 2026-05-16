from django.test import SimpleTestCase
from unittest.mock import MagicMock
from courses.serializers.instructor import (
    InstructorSerializer,
    InstructorDetailSerializer,
    InstructorListSerializer,
    TeacherDetailSerializer,
)


# Tüm instructor serializer'ları için birim testler
# Sadece get_photo ve get_thumbnail metodlarını test ediyoruz
class InstructorSerializerTest(SimpleTestCase):

    def setUp(self):
        self.instructor_serializer = InstructorSerializer()
        self.detail_serializer = InstructorDetailSerializer()
        self.list_serializer = InstructorListSerializer()
        self.teacher_detail_serializer = TeacherDetailSerializer()

    def _make_image(self, path):
        # mock image objesi oluşturur
        image = MagicMock()
        image.name = path
        return image

    def _make_instructor(self, photo_path=None, thumbnail_path=None):
        # mock Instructor objesi oluşturur
        instructor = MagicMock()
        instructor.photo = self._make_image(photo_path) if photo_path else None
        instructor.thumbnail = self._make_image(thumbnail_path) if thumbnail_path else None
        return instructor

    # --- get_photo Testleri ---

    def test_photo_stripping_logic(self):
        # farklı serializer'larda photo path'inden sadece dosya adını döndürmeli
        cases = [
            ("assets/img/photo.jpg", "photo.jpg"),
            ("media/instructors/2026/profile.png", "profile.png"),
            ("simple.jpg", "simple.jpg"),
        ]
        for path, expected in cases:
            with self.subTest(path=path):
                instructor = self._make_instructor(photo_path=path)
                self.assertEqual(self.instructor_serializer.get_photo(instructor), expected)
                self.assertEqual(self.detail_serializer.get_photo(instructor), expected)
                self.assertEqual(self.teacher_detail_serializer.get_photo(instructor), expected)

    def test_photo_returns_none_when_missing(self):
        # photo yoksa None döndürmeli
        instructor = self._make_instructor()
        self.assertIsNone(self.instructor_serializer.get_photo(instructor))
        self.assertIsNone(self.detail_serializer.get_photo(instructor))
        self.assertIsNone(self.teacher_detail_serializer.get_photo(instructor))

    # --- get_thumbnail Testleri ---

    def test_thumbnail_stripping_logic(self):
        # farklı serializer'larda thumbnail path'inden sadece dosya adını döndürmeli
        cases = [
            ("assets/img/thumb.jpg", "thumb.jpg"),
            ("media/instructors/bg/banner.png", "banner.png"),
            ("simple.png", "simple.png"),
        ]
        for path, expected in cases:
            with self.subTest(path=path):
                instructor = self._make_instructor(thumbnail_path=path)
                self.assertEqual(self.detail_serializer.get_thumbnail(instructor), expected)
                self.assertEqual(self.list_serializer.get_thumbnail(instructor), expected)
                self.assertEqual(self.teacher_detail_serializer.get_thumbnail(instructor), expected)

    def test_thumbnail_returns_none_when_missing(self):
        # thumbnail yoksa None döndürmeli
        instructor = self._make_instructor()
        self.assertIsNone(self.detail_serializer.get_thumbnail(instructor))
        self.assertIsNone(self.list_serializer.get_thumbnail(instructor))
        self.assertIsNone(self.teacher_detail_serializer.get_thumbnail(instructor))