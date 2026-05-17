"""
Test Case #281 / Task #281 - Events module integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/281

Goal:
Verify the Events API works with the database, serializers, selectors,
authentication, and event registration service together.

Flow:
1. Create future event records in the test database
2. Request event listing, upcoming events, and event detail endpoints
3. Register an authenticated user for an event
4. Verify duplicate registration is rejected by the API
5. Verify unauthenticated registration is blocked
"""

from datetime import time, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from events.models import Event, EventRegistration
from users.services.auth import generate_tokens


User = get_user_model()


class EventIntegrationTests(APITestCase):
    def setUp(self):
        self.event = self._create_event(
            title="DevOps Workshop",
            slug="devops-workshop",
            days_from_now=3,
            category="Workshop",
        )
        self.second_event = self._create_event(
            title="Cloud Seminar",
            slug="cloud-seminar",
            days_from_now=7,
            category="Seminar",
        )
        self.user = User.objects.create_user(
            username="eventuser",
            email="eventuser@example.com",
            password="StrongPass123!",
        )

    def _create_event(self, title, slug, days_from_now, category):
        return Event.objects.create(
            title=title,
            slug=slug,
            description=f"{title} description",
            requirements="Bring a laptop",
            requirements_list=["Laptop", "Notebook"],
            date=timezone.now() + timedelta(days=days_from_now),
            start_time=time(10, 0),
            end_time=time(12, 0),
            location="Main Hall",
            hall_number="A1",
            is_online=False,
            category=category,
            language="English",
            phone="+905551112233",
            email="events@example.com",
        )

    def _authenticate(self, user=None):
        access_token, _, _ = generate_tokens(user or self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_event_list_returns_events_from_database(self):
        response = self.client.get(reverse("event-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [event["title"] for event in response.data["payload"]["results"]]
        self.assertIn(self.event.title, titles)
        self.assertIn(self.second_event.title, titles)

    def test_upcoming_event_list_returns_serialized_home_event_data(self):
        response = self.client.get(reverse("upcoming-event-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_event = response.data["payload"]["results"][0]
        self.assertIn("timeRange", first_event)
        self.assertEqual(first_event["timeRange"], "10:00 - 12:00")
        self.assertIn(first_event["slug"], {self.event.slug, self.second_event.slug})

    def test_event_detail_returns_event_by_slug(self):
        response = self.client.get(
            reverse("event-detail", kwargs={"slug": self.event.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.event.slug)
        self.assertEqual(response.data["title"], self.event.title)
        self.assertEqual(response.data["requirements_list"], ["Laptop", "Notebook"])

    def test_authenticated_user_can_register_for_event(self):
        self._authenticate()

        response = self.client.post(
            reverse("event-register", kwargs={"slug": self.event.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["errorMessage"])
        self.assertEqual(response.data["payload"]["event"], self.event.id)
        self.assertTrue(
            EventRegistration.objects.filter(
                user=self.user,
                event=self.event,
            ).exists()
        )

    def test_duplicate_event_registration_is_rejected(self):
        EventRegistration.objects.create(user=self.user, event=self.event)
        self._authenticate()

        response = self.client.post(
            reverse("event-register", kwargs={"slug": self.event.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errorMessage"]["detail"],
            "You are already registered for this event.",
        )
        self.assertEqual(
            EventRegistration.objects.filter(user=self.user, event=self.event).count(),
            1,
        )

    def test_unauthenticated_user_cannot_register_for_event(self):
        response = self.client.post(
            reverse("event-register", kwargs={"slug": self.event.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(EventRegistration.objects.filter(event=self.event).exists())
