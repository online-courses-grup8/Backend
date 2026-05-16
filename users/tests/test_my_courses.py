from django.test import SimpleTestCase
from unittest.mock import MagicMock, patch
from users.serializers.my_courses import MyCourseSerializer, MyCourseLessonSerializer


# MyCourseSerializer için birim testler
class MyCourseSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = MyCourseSerializer()

    def _make_enrollment(self, lesson_count=0):
        # mock Enrollment objesi oluşturur
        enrollment = MagicMock()
        enrollment.lesson_count = lesson_count
        return enrollment

    # --- get_completion_percentage Testleri ---

    @patch('users.serializers.my_courses.LessonProgress.objects.filter')
    def test_completion_percentage_zero_when_no_lessons(self, mock_filter):
        # ders yoksa yüzde 0 dönmeli
        enrollment = self._make_enrollment(lesson_count=0)
        result = self.serializer.get_completion_percentage(enrollment)
        self.assertEqual(result, 0)
        mock_filter.assert_not_called()

    @patch('users.serializers.my_courses.LessonProgress.objects.filter')
    def test_completion_percentage_calculation(self, mock_filter):
        # 6 dersin 2'si tamamlanınca 33 dönmeli
        mock_filter.return_value.count.return_value = 2
        enrollment = self._make_enrollment(lesson_count=6)
        result = self.serializer.get_completion_percentage(enrollment)
        self.assertEqual(result, 33)

    @patch('users.serializers.my_courses.LessonProgress.objects.filter')
    def test_completion_percentage_full(self, mock_filter):
        # tüm dersler tamamlanınca 100 dönmeli
        mock_filter.return_value.count.return_value = 3
        enrollment = self._make_enrollment(lesson_count=3)
        result = self.serializer.get_completion_percentage(enrollment)
        self.assertEqual(result, 100)

    @patch('users.serializers.my_courses.LessonProgress.objects.filter')
    def test_completion_percentage_rounding(self, mock_filter):
        # 3 dersin 1'i tamamlanınca yuvarlama mantığını kontrol et
        # 1/3 = 0.333... -> round(33.33) = 33 olmalı
        mock_filter.return_value.count.return_value = 1
        enrollment = self._make_enrollment(lesson_count=3)
        result = self.serializer.get_completion_percentage(enrollment)
        self.assertEqual(result, 33)


# MyCourseLessonSerializer için birim testler
class MyCourseLessonSerializerTest(SimpleTestCase):

    def _make_lesson(self, lesson_id):
        # mock CourseLesson objesi oluşturur
        lesson = MagicMock()
        lesson.id = lesson_id
        return lesson

    def _get_serializer(self, completed_ids):
        # context ile serializer oluşturur
        return MyCourseLessonSerializer(context={'completed_lesson_ids': completed_ids})

    # --- get_is_completed Testleri ---

    def test_lesson_is_completed_when_in_context(self):
        # lesson id context listesinde varsa True dönmeli
        serializer = self._get_serializer(completed_ids=[1, 2, 3])
        lesson = self._make_lesson(lesson_id=2)
        self.assertTrue(serializer.get_is_completed(lesson))

    def test_lesson_is_not_completed_when_not_in_context(self):
        # lesson id context listesinde yoksa False dönmeli
        serializer = self._get_serializer(completed_ids=[1, 3])
        lesson = self._make_lesson(lesson_id=2)
        self.assertFalse(serializer.get_is_completed(lesson))

    def test_lesson_is_not_completed_when_context_empty(self):
        # context listesi boşsa False dönmeli
        serializer = self._get_serializer(completed_ids=[])
        lesson = self._make_lesson(lesson_id=1)
        self.assertFalse(serializer.get_is_completed(lesson))