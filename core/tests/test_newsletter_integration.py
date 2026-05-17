"""
Test Case #275 / Task #275 - Core newsletter integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/275

Goal:
Verify the newsletter subscription endpoint through the API view, serializer,
service layer, and database.

Flow:
1. Send a valid newsletter subscription request
2. Verify the API returns 201 with the success message
3. Verify the subscriber email is persisted in the test database
4. Verify duplicate email subscriptions return validation errors
5. Verify invalid email inputs are rejected

./venv/bin/python manage.py test core.tests -v 2
./venv/bin/python manage.py test -v 2
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models.newsletter import NewsletterSubscriber


class NewsletterIntegrationTest(APITestCase):
    def setUp(self):
        self.newsletter_url = reverse("newsletter-subscribe")

    def test_newsletter_subscription_with_valid_email_creates_subscriber(self):
        response = self.client.post(
            self.newsletter_url,
            {"email": "student@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 201)
        self.assertEqual(response.data["payload"]["message"], "Başarıyla abone oldunuz.")
        self.assertIsNone(response.data["errorMessage"])
        self.assertTrue(
            NewsletterSubscriber.objects.filter(email="student@example.com").exists()
        )

    def test_newsletter_subscription_rejects_duplicate_email_without_creating_second_record(self):
        NewsletterSubscriber.objects.create(email="student@example.com")

        response = self.client.post(
            self.newsletter_url,
            {"email": "student@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], 400)
        self.assertIsNone(response.data["payload"])
        self.assertIn("email", response.data["errorMessage"])
        self.assertEqual(
            NewsletterSubscriber.objects.filter(email="student@example.com").count(),
            1,
        )

    def test_newsletter_subscription_with_invalid_email_is_rejected(self):
        response = self.client.post(
            self.newsletter_url,
            {"email": "invalid-email"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["errorMessage"])
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)
