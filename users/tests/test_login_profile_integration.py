"""
Test Case #258 / Task #258 - Login and profile integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/258

Goal:
Verify the backend integration flow for login and profile management with
authorized access, token generation, password changes, and profile image uploads.

Flow:
1. Log in with correct credentials and verify access/refresh token generation
2. Use the access token to view the authenticated user's profile
3. Update profile fields with authorized access
4. Upload a profile image as a base64 payload and verify it is saved
5. Change the user's password with authorized access
6. Verify protected profile endpoints reject unauthenticated requests

./venv/bin/python manage.py test users.tests.test_profile users.tests.test_login_profile_integration -v 2
"""

import base64
import shutil
import tempfile
from io import BytesIO

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class LoginProfileIntegrationTest(APITestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.storage_override = override_settings(
            MEDIA_ROOT=self.media_root,
            STORAGES={
                "default": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage",
                },
                "staticfiles": {
                    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
                },
            },
        )
        self.storage_override.enable()

        self.login_url = reverse("auth-login")
        self.profile_url = reverse("profile")
        self.profile_update_url = reverse("profile-update")
        self.change_password_url = reverse("change-password")
        self.user = User.objects.create_user(
            username="ayse@example.com",
            email="ayse@example.com",
            password="OldPass1!",
            first_name="Ayse",
            last_name="Yilmaz",
            phone_number="+90 555 111 2233",
        )

    def tearDown(self):
        self.storage_override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def _login(self, password="OldPass1!"):
        return self.client.post(
            self.login_url,
            {"email": self.user.email, "password": password},
            format="json",
        )

    def _authenticate(self):
        response = self._login()
        access_token = response.data["payload"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return access_token

    def _base64_profile_image(self):
        image = Image.new("RGB", (1, 1), color=(255, 0, 0))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    def test_login_with_correct_credentials_returns_valid_access_and_refresh_tokens(self):
        response = self._login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 200)
        self.assertIsNone(response.data["errorMessage"])

        payload = response.data["payload"]
        access_payload = jwt.decode(payload["access"], settings.SECRET_KEY, algorithms=["HS256"])
        refresh_payload = jwt.decode(payload["refresh"], settings.SECRET_KEY, algorithms=["HS256"])

        self.assertEqual(payload["user"]["email"], self.user.email)
        self.assertEqual(access_payload["type"], "access")
        self.assertEqual(access_payload["user_id"], self.user.id)
        self.assertEqual(access_payload["email"], self.user.email)
        self.assertEqual(refresh_payload["type"], "refresh")
        self.assertEqual(refresh_payload["user_id"], self.user.id)
        self.assertIn("expires_at", payload)

    def test_authorized_user_can_view_profile(self):
        self._authenticate()

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 200)
        self.assertEqual(response.data["payload"]["email"], self.user.email)
        self.assertEqual(response.data["payload"]["first_name"], "Ayse")
        self.assertEqual(response.data["payload"]["profile_image"], "anonymous.jpeg")

    def test_authorized_user_can_update_profile_fields_and_profile_image(self):
        self._authenticate()

        response = self.client.patch(
            self.profile_update_url,
            {
                "first_name": "Aylin",
                "last_name": "Demir",
                "phone_number": "+90 555 999 8877",
                "profile_image": self._base64_profile_image(),
            },
            format="json",
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 200)
        self.assertEqual(response.data["payload"]["first_name"], "Aylin")
        self.assertEqual(response.data["payload"]["last_name"], "Demir")
        self.assertEqual(response.data["payload"]["phone_number"], "+90 555 999 8877")
        self.assertEqual(response.data["payload"]["profile_image"], "aylin_demir.png")
        self.assertEqual(self.user.first_name, "Aylin")
        self.assertEqual(self.user.last_name, "Demir")
        self.assertEqual(self.user.phone_number, "+90 555 999 8877")
        self.assertTrue(self.user.profile_image.name.endswith("aylin_demir.png"))

    def test_authorized_user_can_change_password_and_login_with_new_password(self):
        self._authenticate()

        response = self.client.put(
            self.change_password_url,
            {
                "current_password": "OldPass1!",
                "new_password": "NewPass1!",
                "confirm_new_password": "NewPass1!",
            },
            format="json",
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password("NewPass1!"))

        self.client.credentials()
        login_response = self._login(password="NewPass1!")

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(login_response.data["payload"]["user"]["email"], self.user.email)

    def test_profile_endpoints_require_authorized_access(self):
        endpoints = [
            ("get", self.profile_url, None),
            ("patch", self.profile_update_url, {"first_name": "Aylin"}),
            ("put", self.change_password_url, {
                "current_password": "OldPass1!",
                "new_password": "NewPass1!",
                "confirm_new_password": "NewPass1!",
            }),
        ]

        for method, url, data in endpoints:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data, format="json")

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
