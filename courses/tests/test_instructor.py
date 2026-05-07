from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Instructor, InstructorSkill


class InstructorListAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # test instructor'ları oluştur
        self.instructor1 = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python, Django',
            bio_softskill='Leadership',
            specialization='Backend Development',
            experience=5,
            position='Senior Developer',
            facebook='https://facebook.com/jane',
            linkedin='https://linkedin.com/in/jane'
        )

        self.instructor2 = Instructor.objects.create(
            name='John Doe',
            bio_hardskill='React, Next.js',
            bio_softskill='Teamwork',
            specialization='Frontend Development',
            experience=3,
            position='Frontend Developer',
        )

    def test_instructor_list_returns_200(self):
        # API 200 dönüyor mu?
        response = self.client.get(reverse('instructor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_instructor_list_unauthenticated(self):
        # login olmadan erişilebiliyor mu?
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('instructor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_instructor_list_count(self):
        # doğru sayıda instructor geliyor mu?
        response = self.client.get(reverse('instructor-list'))
        self.assertEqual(response.data['count'], 2)

    def test_instructor_list_required_fields(self):
        # gerekli alanlar var mı?
        response = self.client.get(reverse('instructor-list'))
        instructor = response.data['results'][0]
        self.assertIn('id', instructor)
        self.assertIn('name', instructor)
        self.assertIn('slug', instructor)
        self.assertIn('photo', instructor)
        self.assertIn('position', instructor)
        self.assertIn('facebook', instructor)
        self.assertIn('instagram', instructor)
        self.assertIn('linkedin', instructor)
        self.assertIn('twitter', instructor)

    def test_instructor_slug_auto_generated(self):
        # slug otomatik oluşturuluyor mu?
        self.assertEqual(self.instructor1.slug, 'jane-cooper')
        self.assertEqual(self.instructor2.slug, 'john-doe')


class InstructorDetailAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # test instructor oluştur
        self.instructor = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python, Django',
            bio_softskill='Leadership',
            specialization='Backend Development',
            experience=5,
            position='Senior Developer',
            phone_number='+1234567890',
            facebook='https://facebook.com/jane',
            linkedin='https://linkedin.com/in/jane'
        )

        # test skill'leri oluştur
        self.skill1 = InstructorSkill.objects.create(
            instructor=self.instructor,
            skill='Python',
            percentage=90
        )
        self.skill2 = InstructorSkill.objects.create(
            instructor=self.instructor,
            skill='Django',
            percentage=85
        )

    def test_instructor_detail_returns_200(self):
        # API 200 dönüyor mu?
        url = reverse('instructor-detail', kwargs={'slug': self.instructor.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_instructor_detail_required_fields(self):
        # gerekli alanlar var mı?
        url = reverse('instructor-detail', kwargs={'slug': self.instructor.slug})
        response = self.client.get(url)
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('slug', response.data)
        self.assertIn('specialization', response.data)
        self.assertIn('experience', response.data)
        self.assertIn('position', response.data)
        self.assertIn('bio_hardskill', response.data)
        self.assertIn('bio_softskill', response.data)
        self.assertIn('skills', response.data)

    def test_instructor_detail_skills(self):
        # skill'ler geliyor mu?
        url = reverse('instructor-detail', kwargs={'slug': self.instructor.slug})
        response = self.client.get(url)
        self.assertEqual(len(response.data['skills']), 2)

    def test_instructor_detail_skill_fields(self):
        # skill alanları doğru mu?
        url = reverse('instructor-detail', kwargs={'slug': self.instructor.slug})
        response = self.client.get(url)
        skill = response.data['skills'][0]
        self.assertIn('skill', skill)
        self.assertIn('percentage', skill)

    def test_instructor_detail_not_found(self):
        # olmayan slug 404 dönüyor mu?
        url = reverse('instructor-detail', kwargs={'slug': 'olmayan-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_instructor_detail_unauthenticated(self):
        # login olmadan erişilebiliyor mu?
        self.client.force_authenticate(user=None)
        url = reverse('instructor-detail', kwargs={'slug': self.instructor.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class InstructorOthersAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # iki instructor oluştur
        self.instructor1 = Instructor.objects.create(
            name='Jane Cooper',
            bio_hardskill='Python, Django',
            bio_softskill='Leadership',
            specialization='Backend Development',
            experience=5,
            position='Senior Developer',
        )

        self.instructor2 = Instructor.objects.create(
            name='John Doe',
            bio_hardskill='React, Next.js',
            bio_softskill='Teamwork',
            specialization='Frontend Development',
            experience=3,
            position='Frontend Developer',
        )

    def test_others_returns_200(self):
        # API 200 dönüyor mu?
        url = reverse('instructor-others', kwargs={'slug': self.instructor1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_others_excludes_current_instructor(self):
        # mevcut instructor hariç tutuluyor mu?
        url = reverse('instructor-others', kwargs={'slug': self.instructor1.slug})
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')

    def test_others_unauthenticated(self):
        # login olmadan erişilebiliyor mu?
        self.client.force_authenticate(user=None)
        url = reverse('instructor-others', kwargs={'slug': self.instructor1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_others_required_fields(self):
        # gerekli alanlar var mı?
        url = reverse('instructor-others', kwargs={'slug': self.instructor1.slug})
        response = self.client.get(url)
        instructor = response.data['results'][0]
        self.assertIn('id', instructor)
        self.assertIn('name', instructor)
        self.assertIn('slug', instructor)
        self.assertIn('position', instructor)