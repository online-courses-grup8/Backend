from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models.faq import FAQ


class FAQListAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # aktif FAQ
        self.active_faq = FAQ.objects.create(
            question="How long do I have access to the courses?",
            answer="You have lifetime access to all course materials.",
            order=1,
            is_active=True,
            is_featured=True
        )

        # pasif FAQ (görünmemeli)
        self.inactive_faq = FAQ.objects.create(
            question="This is an inactive question?",
            answer="This answer should not appear in the API.",
            order=2,
            is_active=False,
            is_featured=False
        )

    def test_faq_list_returns_200(self):
        # API 200 dönüyor mu?
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_active_faqs_returned(self):
        # sadece aktif FAQ'lar geliyor mu?
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.data['count'], 1)

    def test_required_fields_in_response(self):
        # gerekli alanlar var mı?
        response = self.client.get(reverse('faq-list'))
        faq = response.data['results'][0]
        self.assertIn('id', faq)
        self.assertIn('question', faq)
        self.assertIn('answer', faq)
        self.assertIn('is_featured', faq)

    def test_unauthenticated_access(self):
        # login olmadan erişilebiliyor mu?
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_faq_ordering(self):
        # FAQ'lar order alanına göre sıralı geliyor mu?
        FAQ.objects.create(
            question="Second question in order?",
            answer="This is the second answer.",
            order=2,
            is_active=True,
            is_featured=False
        )
        response = self.client.get(reverse('faq-list'))
        results = response.data['results']
        self.assertLess(results[0]['id'], results[1]['id'])