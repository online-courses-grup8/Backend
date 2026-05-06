from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Category, Instructor, Course, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseCommentCreateTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # test kategorisi
        self.category = Category.objects.create(
            name='Development',
            slug='development'
        )

        # test instructor
        self.instructor = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python',
            bio_softskill='Leadership',
            specialization='Backend',
            experience=5,
            position='Developer'
        )

        # yayında olan kurs
        self.course = Course.objects.create(
            title='Web Development',
            slug='web-development',
            description='Test course',
            price=59.00,
            duration=510,
            level='expert',
            language='English',
            rating=4.5,
            is_published=True,
            category=self.category,
            instructor=self.instructor
        )

        # yayında olmayan kurs
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

        # test kullanıcısı
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

        self.url = reverse('course-comment-create', kwargs={'slug': self.course.slug})

    def test_guest_user_can_comment(self):
        # login olmadan yorum yapılabiliyor mu?
        data = {
            'name': 'Guest User',
            'email': 'guest@test.com',
            'message': 'Great course!',
            'rating': 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_comment(self):
        # login kullanıcı yorum yapabiliyor mu?
        self.client.force_authenticate(user=self.user)
        data = {
            'message': 'Great course!',
            'rating': 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_guest_without_name_fails(self):
        # guest kullanıcı name vermeden yorum yapamaz
        data = {
            'email': 'guest@test.com',
            'message': 'Great course!',
            'rating': 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_without_email_fails(self):
        # guest kullanıcı email vermeden yorum yapamaz
        data = {
            'name': 'Guest User',
            'message': 'Great course!',
            'rating': 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_must_be_between_1_and_5(self):
        # rating 1-5 arasında olmalı
        data = {
            'name': 'Guest User',
            'email': 'guest@test.com',
            'message': 'Great course!',
            'rating': 6  # geçersiz rating
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_on_unpublished_course_fails(self):
        # yayında olmayan kursa yorum yapılamaz
        url = reverse('course-comment-create', kwargs={'slug': self.unpublished_course.slug})
        data = {
            'name': 'Guest User',
            'email': 'guest@test.com',
            'message': 'Great course!',
            'rating': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_name_taken_from_account(self):
        # login kullanıcının adı otomatik alınıyor mu?
        self.client.force_authenticate(user=self.user)
        data = {
            'message': 'Great course!',
            'rating': 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # DB'de kullanıcı adı doğru kaydedilmiş mi?
        comment = Comment.objects.last()
        self.assertEqual(comment.email, self.user.email)