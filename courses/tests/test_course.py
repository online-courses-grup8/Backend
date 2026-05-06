from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Category, Instructor, Course, CourseSection, CourseLesson, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()  # custom User modelimizi kullan


class CourseListAPITest(TestCase):

    def setUp(self):
        # her testten önce çalışır, test verilerini oluşturur
        self.client = APIClient()

        # test kategorisi oluştur
        self.category = Category.objects.create(
            name='Development',
            slug='development'
        )

        # test instructor oluştur
        self.instructor = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python, Django',
            bio_softskill='Leadership',
            specialization='Backend Development',
            experience=5,
            position='Senior Developer'
        )

        # yayında olan test kursu oluştur
        self.published_course = Course.objects.create(
            title='Web Development',
            slug='web-development',
            description='Web development course',
            price=59.00,
            duration=510,  # dakika cinsinden
            level='expert',
            language='English',
            rating=4.5,
            is_published=True,  # yayında
            category=self.category,
            instructor=self.instructor
        )

        # yayında olmayan test kursu oluştur
        self.unpublished_course = Course.objects.create(
            title='Unpublished Course',
            slug='unpublished-course',
            description='This course is not published',
            price=29.00,
            duration=200,
            level='beginner',
            language='English',
            rating=0.0,
            is_published=False,  # yayında değil
            category=self.category,
            instructor=self.instructor
        )

        # test kullanıcısı oluştur
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

        # kursa bölüm ve ders ekle
        self.section = CourseSection.objects.create(
            course=self.published_course,
            title='Section 1',
            order=1
        )
        self.lesson = CourseLesson.objects.create(
            section=self.section,
            title='Lesson 1',
            duration=30,
            order=1
        )
        # kullanıcıyı kursa kaydet
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.published_course
        )

    def test_course_list_returns_200(self):
        # API 200 dönüyor mu?
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_list_unauthenticated(self):
        # login olmadan erişilebiliyor mu?
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_published_courses_returned(self):
        # sadece yayında olan kurslar geliyor mu?
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.data['count'], 1)  # sadece 1 kurs olmalı

    def test_required_fields_in_response(self):
        # response'da gerekli alanlar var mı?
        response = self.client.get(reverse('course-list'))
        course = response.data['results'][0]
        self.assertIn('title', course)
        self.assertIn('price', course)
        self.assertIn('level', course)
        self.assertIn('duration', course)
        self.assertIn('rating', course)
        self.assertIn('student_count', course)
        self.assertIn('lesson_count', course)
        self.assertIn('instructor', course)

    def test_student_count_is_correct(self):
        # student_count doğru hesaplanıyor mu?
        response = self.client.get(reverse('course-list'))
        course = response.data['results'][0]
        self.assertEqual(course['student_count'], 1)  # 1 enrollment var

    def test_lesson_count_is_correct(self):
        # lesson_count doğru hesaplanıyor mu?
        response = self.client.get(reverse('course-list'))
        course = response.data['results'][0]
        self.assertEqual(course['lesson_count'], 1)  # 1 ders var