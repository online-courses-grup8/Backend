"""
Test Case #278 / Task #278 - Payments module checkout integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/278

Goal:
Verify the checkout API flow through authentication, cart data, payment service,
payment records, payment items, enrollment creation, and cart cleanup.

Flow:
1. Authenticate a user with a JWT access token
2. Add courses to the user's cart
3. Submit checkout with valid card_last_four data
4. Verify payment and payment item records are created
5. Verify course enrollments are created
6. Verify the cart is cleared after successful checkout
7. Verify empty carts and invalid card data are rejected
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Category, Course, Enrollment, Instructor
from payments.models import CartItem, Payment, PaymentItem
from payments.services.cart import add_to_cart
from users.services.auth import generate_tokens


User = get_user_model()


class CheckoutIntegrationTest(APITestCase):
    def setUp(self):
        self.checkout_url = reverse("checkout")
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
        self.first_course = self._create_course("Docker Basics", "docker-basics", "49.99")
        self.second_course = self._create_course("Kubernetes Basics", "kubernetes-basics", "59.99")

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

    def test_checkout_with_cart_creates_payment_enrollments_and_clears_cart(self):
        self._authenticate()
        add_to_cart(self.user, self.first_course.id)
        add_to_cart(self.user, self.second_course.id)

        response = self.client.post(
            self.checkout_url,
            {"card_last_four": "1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 201)
        self.assertIsNone(response.data["errorMessage"])

        payment = Payment.objects.get(user=self.user)
        payment_payload = response.data["payload"]["payment"]

        self.assertEqual(payment.status, "completed")
        self.assertEqual(payment.amount, Decimal("109.98"))
        self.assertEqual(payment.card_last_four, "1234")
        self.assertEqual(payment_payload["transaction_id"], payment.transaction_id)
        self.assertEqual(Decimal(str(payment_payload["amount"])), Decimal("109.98"))
        self.assertEqual(payment_payload["status"], "completed")
        self.assertEqual(response.data["payload"]["enrolled_courses"], [self.first_course.id, self.second_course.id])

        self.assertEqual(PaymentItem.objects.filter(payment=payment).count(), 2)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.first_course).exists())
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.second_course).exists())
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 0)

    def test_checkout_with_empty_cart_returns_validation_error(self):
        self._authenticate()

        response = self.client.post(
            self.checkout_url,
            {"card_last_four": "1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], 400)
        self.assertEqual(response.data["errorMessage"]["detail"], "Your cart is empty.")
        self.assertEqual(Payment.objects.count(), 0)

    def test_checkout_with_invalid_card_last_four_is_rejected(self):
        self._authenticate()
        add_to_cart(self.user, self.first_course.id)

        response = self.client.post(
            self.checkout_url,
            {"card_last_four": "12AB"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("card_last_four", response.data["errorMessage"])
        self.assertEqual(Payment.objects.count(), 0)
        self.assertEqual(CartItem.objects.filter(cart__user=self.user).count(), 1)

    def test_checkout_requires_authentication(self):
        response = self.client.post(
            self.checkout_url,
            {"card_last_four": "1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
