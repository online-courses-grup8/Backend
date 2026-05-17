"""
Test Case #255 / Task #255 - Registration feature integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/255

Goal:
Verify the user registration endpoint with database connection and integration
between the API view, serializer, service layer, user model, and JWT authentication.

Flow:
1. Send a valid registration request to the backend API
2. Verify the response status, payload, user data, and generated JWT tokens
3. Verify the registered user is saved in the test database
4. Use the returned access token to access the protected profile endpoint
5. Verify duplicate email registration returns a validation error
6. Verify missing required fields return validation errors
7. Verify password mismatch returns a validation error
"""

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class RegisterIntegrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("auth-register")
        self.profile_url = reverse("profile")

    def _valid_payload(self):
        return {
            "first_name": "Ayse",
            "last_name": "Yilmaz",
            "email": "ayse.yilmaz@example.com",
            "password": "Password1",
            "confirm_password": "Password1",
            "phone_number": "+90 555 123 4567",
        }

    def test_register_with_valid_data_creates_user_returns_tokens_and_authenticates_profile(self):
        # View, serializer, service, model ve JWT authentication zincirini birlikte test eder.
        response = self.client.post(self.register_url, self._valid_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 201)
        self.assertIsNone(response.data["errorMessage"])

        payload = response.data["payload"]
        user = User.objects.get(email="ayse.yilmaz@example.com")

        self.assertEqual(payload["user"]["id"], user.id)
        self.assertEqual(payload["user"]["email"], user.email)
        self.assertEqual(user.first_name, "Ayse")
        self.assertEqual(user.last_name, "Yilmaz")
        self.assertEqual(user.phone_number, "+90 555 123 4567")
        self.assertEqual(user.username, user.email)
        self.assertTrue(user.check_password("Password1"))

        access_payload = jwt.decode(payload["access"], settings.SECRET_KEY, algorithms=["HS256"])
        refresh_payload = jwt.decode(payload["refresh"], settings.SECRET_KEY, algorithms=["HS256"])

        self.assertEqual(access_payload["type"], "access")
        self.assertEqual(access_payload["user_id"], user.id)
        self.assertEqual(access_payload["email"], user.email)
        self.assertEqual(refresh_payload["type"], "refresh")
        self.assertEqual(refresh_payload["user_id"], user.id)
        self.assertIn("expires_at", payload)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {payload['access']}")
        profile_response = self.client.get(self.profile_url)

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["payload"]["email"], user.email)

    def test_register_with_duplicate_email_returns_validation_error_without_creating_user(self):
        User.objects.create_user(
            username="ayse.yilmaz@example.com",
            email="ayse.yilmaz@example.com",
            password="Password1",
        )

        response = self.client.post(self.register_url, self._valid_payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], 400)
        self.assertIsNone(response.data["payload"])
        self.assertIn("email", response.data["errorMessage"])
        self.assertEqual(User.objects.filter(email="ayse.yilmaz@example.com").count(), 1)

    def test_register_with_missing_required_fields_returns_validation_errors(self):
        required_fields = ["email", "password", "confirm_password"]

        for field in required_fields:
            with self.subTest(field=field):
                payload = self._valid_payload()
                payload.pop(field)

                response = self.client.post(self.register_url, payload, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data["status"], 400)
                self.assertIsNone(response.data["payload"])
                self.assertIn(field, response.data["errorMessage"])
                self.assertFalse(User.objects.filter(email=payload.get("email")).exists())

    def test_register_with_password_mismatch_returns_validation_error_without_creating_user(self):
        payload = self._valid_payload()
        payload["confirm_password"] = "Password2"

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], 400)
        self.assertIsNone(response.data["payload"])
        self.assertIn("confirm_password", response.data["errorMessage"])
        self.assertFalse(User.objects.filter(email=payload["email"]).exists())
