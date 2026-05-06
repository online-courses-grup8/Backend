from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Category, Instructor, Course, CourseSection, CourseLesson, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseDetailTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(
            name='Development',
            slug='development'
        )

        self.instructor = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python, Django',
            bio_softskill='Leadership',
            specialization='Backend Development',
            experience=5,
            position='Senior Developer'
        )

        self.course = Course.objects.create(
            title='Web Development',
            slug='web-development',
            description='Web development course',
            price=59.00,
            duration=510,
            level='expert',
            language='English',
            rating=4.5,
            is_published=True,
            category=self.category,
            instructor=self.instructor
        )

        self.unpublished_course = Course.objects.create(
            title='Unpublished Course',
            slug='unpublished-course',
            description='Test course',
            price=29.00,
            duration=200,
            level='beginner',
            language='English',
            rating=0.0,
            is_published=False,
            category=self.category,
            instructor=self.instructor
        )

        # bölüm ve ders ekle
        self.section = CourseSection.objects.create(
            course=self.course,
            title='Section 1',
            order=1
        )
        self.lesson = CourseLesson.objects.create(
            section=self.section,
            title='Lesson 1',
            duration=30,
            order=1,
            is_free=True
        )

        # yorum ekle
        self.comment = Comment.objects.create(
            course=self.course,
            name='Test User',
            email='test@test.com',
            message='Great course!',
            rating=5
        )


    # --- OVERVIEW TESTLERI ---

    def test_overview_returns_200(self):
        # overview endpoint 200 dönüyor mu?
        url = reverse('course-overview', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_overview_required_fields(self):
        # response'da gerekli alanlar var mı?
        url = reverse('course-overview', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)
        self.assertIn('level', response.data)
        self.assertIn('duration', response.data)
        self.assertIn('student_count', response.data)
        self.assertIn('lesson_count', response.data)

    def test_overview_unpublished_returns_404(self):
        # yayında olmayan kurs 404 dönüyor mu?
        url = reverse('course-overview', kwargs={'slug': self.unpublished_course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # --- CURRICULUM TESTLERI ---

    def test_curriculum_returns_200(self):
        # curriculum endpoint 200 dönüyor mu?
        url = reverse('course-curriculum', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_curriculum_has_sections(self):
        # response'da section var mı?
        url = reverse('course-curriculum', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)  # 1 section var

    def test_curriculum_has_lessons(self):
        # section içinde lesson var mı?
        url = reverse('course-curriculum', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(len(response.data[0]['lessons']), 1)  # 1 lesson var


    # --- INSTRUCTOR TESTLERI ---

    def test_instructor_returns_200(self):
        # instructor endpoint 200 dönüyor mu?
        url = reverse('course-instructor', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_instructor_required_fields(self):
        # response'da gerekli alanlar var mı?
        url = reverse('course-instructor', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertIn('name', response.data)
        self.assertIn('specialization', response.data)
        self.assertIn('experience', response.data)
        self.assertIn('bio_hardskill', response.data)
        self.assertIn('bio_softskill', response.data)


    # --- REVIEWS TESTLERI ---

    def test_reviews_returns_200(self):
        # reviews endpoint 200 dönüyor mu?
        url = reverse('course-reviews', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reviews_has_required_fields(self):
        # response'da gerekli alanlar var mı?
        url = reverse('course-reviews', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertIn('average_rating', response.data)
        self.assertIn('total_reviews', response.data)
        self.assertIn('rating_distribution', response.data)
        self.assertIn('reviews', response.data)

    def test_reviews_average_rating_correct(self):
        # average rating doğru hesaplanıyor mu?
        url = reverse('course-reviews', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.data['average_rating'], 5.0)  # 1 yorum, rating=5

    def test_reviews_total_correct(self):
        # toplam yorum sayısı doğru mu?
        url = reverse('course-reviews', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.data['total_reviews'], 1)  # 1 yorum var