"""
Test Case #275 / Task #275 - Core contact integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/275

Goal:
Verify the contact form submission endpoint through the API view, serializer,
service layer, and database.

Flow:
1. Send a valid contact form submission request
2. Verify the API returns 201 with the saved message payload
3. Verify the contact message is persisted in the test database
4. Verify missing required fields return validation errors
5. Verify invalid email and short message inputs are rejected
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models.contact import ContactMessage


class ContactMessageIntegrationTest(APITestCase):
    def setUp(self):
        self.contact_url = reverse("contact-create")
        self.valid_payload = {
            "name": "Ayse Yilmaz",
            "email": "ayse@example.com",
            "message": "Bu mesaj test icin yeterince uzun bir mesajdir.",
        }

    def test_contact_submission_with_valid_data_creates_message(self):
        response = self.client.post(self.contact_url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 201)
        self.assertIsNone(response.data["errorMessage"])

        message = ContactMessage.objects.get(email="ayse@example.com")

        self.assertEqual(response.data["payload"]["id"], message.id)
        self.assertEqual(message.name, "Ayse Yilmaz")
        self.assertEqual(message.email, "ayse@example.com")
        self.assertEqual(message.message, "Bu mesaj test icin yeterince uzun bir mesajdir.")

    def test_contact_submission_with_missing_required_fields_returns_validation_errors(self):
        required_fields = ["name", "email", "message"]

        for field in required_fields:
            with self.subTest(field=field):
                payload = self.valid_payload.copy()
                payload.pop(field)

                response = self.client.post(self.contact_url, payload, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data["status"], 400)
                self.assertIsNone(response.data["payload"])
                self.assertIn(field, response.data["errorMessage"])
                self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_submission_with_invalid_email_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["email"] = "invalid-email"

        response = self.client.post(self.contact_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["errorMessage"])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_submission_with_short_message_is_rejected(self):
        payload = self.valid_payload.copy()
        payload["message"] = "short"

        response = self.client.post(self.contact_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data["errorMessage"])
        self.assertEqual(ContactMessage.objects.count(), 0)
