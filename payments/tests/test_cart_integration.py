"""
Test Case #278 / Task #278 - Payments module cart integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/278

Goal:
Verify the cart API flow through authentication, views, serializers, services,
selectors, and database records.

Flow:
1. Authenticate a user with a JWT access token
2. Add a course to the authenticated user's cart
3. Verify cart listing returns item details, total price, and item count
4. Verify duplicate and already-owned courses are rejected
5. Verify cart sync groups added, already-in-cart, and already-owned courses
6. Verify cart item removal deletes the record
7. Verify cart endpoints reject unauthenticated requests
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course, Enrollment, Instructor
from payments.models import CartItem
from users.services.auth import generate_tokens


User = get_user_model()


class CartIntegrationTest(APITestCase):
    def setUp(self):
        self.cart_url = reverse("cart")
        self.cart_add_url = reverse("cart-add")
        self.cart_sync_url = reverse("cart-sync")
        self.user = User.objects.create_user(
            username="student@example.com",
            email="student@example.com",
            password="Password1!",
        )
        self.category = Category.objects.create(name="DevOps", slug="devops")
        self.instructor = Instructor.objects.create(
            name="Jane Doe",
            bio_hardskill="Cloud and automation",
            bio_softskill="Mentoring",
            specialization="DevOps",
        )
        self.course = self._create_course("Docker Basics", "docker-basics", "49.99")
        self.second_course = self._create_course("Kubernetes Basics", "kubernetes-basics", "59.99")
        self.owned_course = self._create_course("Owned Course", "owned-course", "39.99")
        Enrollment.objects.create(user=self.user, course=self.owned_course)

    def _create_course(self, title, slug, price):
        return Course.objects.create(
            title=title,
            slug=slug,
            description="A complete course description for integration testing.",
            thumbnail="assets/img/course.jpg",
            price=Decimal(price),
            duration=120,
            level="beginner",
            language="English",
            certification=True,
            is_published=True,
            category=self.category,
            instructor=self.instructor,
        )

    def _authenticate(self):
        access_token, _, _ = generate_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_authenticated_user_can_add_and_view_cart_item(self):
        self._authenticate()

        add_response = self.client.post(
            self.cart_add_url,
            {"course_id": self.course.id},
            format="json",
        )
        list_response = self.client.get(self.cart_url)

        self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(add_response.data["status"], 201)
        self.assertIsNone(add_response.data["errorMessage"])
        self.assertEqual(add_response.data["payload"]["course_id"], self.course.id)
        self.assertEqual(add_response.data["payload"]["course_title"], self.course.title)
        self.assertEqual(add_response.data["payload"]["course_slug"], self.course.slug)
        self.assertEqual(add_response.data["payload"]["thumbnail"], "course.jpg")

        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 1)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["payload"]["item_count"], 1)
        self.assertEqual(list_response.data["payload"]["items"][0]["course_id"], self.course.id)
        self.assertEqual(Decimal(str(list_response.data["payload"]["total"])), Decimal("49.99"))

    def test_add_to_cart_rejects_duplicate_and_already_owned_courses(self):
        self._authenticate()
        self.client.post(self.cart_add_url, {"course_id": self.course.id}, format="json")

        duplicate_response = self.client.post(
            self.cart_add_url,
            {"course_id": self.course.id},
            format="json",
        )
        owned_response = self.client.post(
            self.cart_add_url,
            {"course_id": self.owned_course.id},
            format="json",
        )

        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(duplicate_response.data["errorMessage"]["detail"], "Course is already in your cart.")
        self.assertEqual(owned_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(owned_response.data["errorMessage"]["detail"], "You already own this course.")
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 1)

    def test_authenticated_user_can_sync_cart_with_added_duplicate_and_owned_results(self):
        self._authenticate()
        self.client.post(self.cart_add_url, {"course_id": self.course.id}, format="json")

        response = self.client.post(
            self.cart_sync_url,
            {
                "course_ids": [
                    self.course.id,
                    self.second_course.id,
                    self.owned_course.id,
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data["payload"]
        self.assertEqual(payload["added"], [self.second_course.id])
        self.assertEqual(payload["already_in_cart"], [self.course.id])
        self.assertEqual(payload["already_owned"], [self.owned_course.id])
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 2)

    def test_authenticated_user_can_remove_cart_item(self):
        self._authenticate()
        add_response = self.client.post(
            self.cart_add_url,
            {"course_id": self.course.id},
            format="json",
        )
        item_id = add_response.data["payload"]["id"]

        response = self.client.delete(reverse("cart-remove", kwargs={"item_id": item_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["message"], "Course removed from cart.")
        self.assertFalse(CartItem.objects.filter(id=item_id).exists())

    def test_cart_endpoints_require_authentication(self):
        endpoints = [
            ("get", self.cart_url, None),
            ("post", self.cart_add_url, {"course_id": self.course.id}),
            ("post", self.cart_sync_url, {"course_ids": [self.course.id]}),
            ("delete", reverse("cart-remove", kwargs={"item_id": 1}), None),
        ]

        for method, url, data in endpoints:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data, format="json")

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
