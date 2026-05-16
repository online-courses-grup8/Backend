from django.test import SimpleTestCase
from unittest.mock import MagicMock
from courses.serializers.course import CourseListSerializer, CourseOverviewSerializer


# CourseListSerializer ve CourseOverviewSerializer için birim testler
# Sadece mantık testi yapıldığı için DB gerektirmez
class CourseThumbnailSerializerTest(SimpleTestCase):

    def setUp(self):
        self.list_serializer = CourseListSerializer()
        self.overview_serializer = CourseOverviewSerializer()

    # Mock bir Course objesi oluşturur
    def _make_course(self, thumbnail_path=None):
        course = MagicMock()
        if thumbnail_path:
            thumbnail = MagicMock()
            thumbnail.name = thumbnail_path
            course.thumbnail = thumbnail
        else:
            course.thumbnail = None
        return course

    # --- Thumbnail Ayıklama Mantığı Testleri ---

    def test_thumbnail_stripping_logic(self):
        # Farklı derinlikteki pathlerden sadece dosya adını döndürmeli
        cases = [
            ("assets/img/course.jpg", "course.jpg"),                        # Standart path
            ("media/courses/2026/thumb.png", "thumb.png"),                  # Derin path
            ("simple.jpg", "simple.jpg"),                                   # Path yok, sadece dosya
            ("media/courses/my course photo v2.jpg", "my course photo v2.jpg"),  # Boşluklu dosya adı
            ("media/img/course_v1-final.jpeg", "course_v1-final.jpeg"),     # Özel karakterli dosya adı
        ]
        for path, expected in cases:
            with self.subTest(path=path):
                course = self._make_course(thumbnail_path=path)
                self.assertEqual(self.list_serializer.get_thumbnail(course), expected)
                self.assertEqual(self.overview_serializer.get_thumbnail(course), expected)

    def test_thumbnail_returns_none_when_missing(self):
        # Thumbnail alanı boşsa her iki serializer da None dönmeli
        course = self._make_course(thumbnail_path=None)
        self.assertIsNone(self.list_serializer.get_thumbnail(course))
        self.assertIsNone(self.overview_serializer.get_thumbnail(course))