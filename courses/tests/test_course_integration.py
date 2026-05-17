"""
Test Case #284 / Task #284 - Courses module integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/284

Goal:
Verify the Courses API works with the database, selectors, serializers,
pagination, curriculum, instructor, review, and comment creation flows together.

Flow:
1. Create category, instructor, published course, draft course, curriculum, enrollment, and reviews
2. Request course listing and verify only published courses are returned with pagination metadata
3. Request overview, curriculum, instructor, reviews, and category-filtered course endpoints
4. Submit a guest course comment through the API
5. Verify created comment data is persisted in the database
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import (
    Category,
    Comment,
    Course,
    CourseLesson,
    CourseSection,
    Enrollment,
    Instructor,
    InstructorSkill,
)


User = get_user_model()


class CourseIntegrationTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="DevOps",
            slug="devops",
            icon="assets/img/devops.png",
        )
        self.other_category = Category.objects.create(
            name="Cloud",
            slug="cloud",
            icon="assets/img/cloud.png",
        )
        self.instructor = Instructor.objects.create(
            name="Ada Lovelace",
            bio_hardskill="Backend and DevOps engineering experience.",
            bio_softskill="Clear communication and mentoring.",
            photo="assets/img/ada-photo.jpg",
            thumbnail="assets/img/ada-thumb.jpg",
            specialization="DevOps Engineer",
            phone_number="+905551112233",
            experience=8,
            position="Senior Instructor",
            linkedin="https://example.com/ada",
        )
        InstructorSkill.objects.create(
            instructor=self.instructor,
            skill="CI/CD",
            percentage=95,
        )
        self.user = User.objects.create_user(
            username="courseuser",
            email="courseuser@example.com",
            password="StrongPass123!",
        )
        self.course = self._create_course(
            title="DevOps Fundamentals",
            slug="devops-fundamentals",
            category=self.category,
            is_published=True,
        )
        self.draft_course = self._create_course(
            title="Draft DevOps Course",
            slug="draft-devops-course",
            category=self.category,
            is_published=False,
        )
        self.other_course = self._create_course(
            title="Cloud Basics",
            slug="cloud-basics",
            category=self.other_category,
            is_published=True,
        )
        self.section = CourseSection.objects.create(
            course=self.course,
            title="Getting Started",
            description="Introductory DevOps section",
            order=1,
        )
        CourseLesson.objects.create(
            section=self.section,
            title="What is DevOps?",
            duration=20,
            order=1,
            is_free=True,
        )
        CourseLesson.objects.create(
            section=self.section,
            title="Pipeline Basics",
            duration=35,
            order=2,
            is_free=False,
        )
        Enrollment.objects.create(user=self.user, course=self.course)
        Comment.objects.create(
            course=self.course,
            user=self.user,
            name="Course User",
            email="courseuser@example.com",
            message="Excellent course content.",
            rating=5,
        )
        Comment.objects.create(
            course=self.course,
            user=None,
            name="Guest Reviewer",
            email="guest@example.com",
            message="Useful examples.",
            rating=4,
        )

    def _create_course(self, title, slug, category, is_published):
        return Course.objects.create(
            title=title,
            slug=slug,
            description=f"{title} description",
            curriculum_description=f"{title} curriculum overview",
            requirements="Basic computer knowledge",
            thumbnail=f"assets/img/{slug}.jpg",
            price=Decimal("49.99"),
            duration=120,
            level="beginner",
            language="English",
            certification=True,
            rating=4.5,
            video_url="https://example.com/video",
            is_published=is_published,
            category=category,
            instructor=self.instructor,
        )

    def test_course_list_returns_only_published_courses_with_pagination(self):
        response = self.client.get(reverse("course-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data["payload"]
        slugs = [course["slug"] for course in payload["results"]]
        listed_course = next(
            course for course in payload["results"] if course["slug"] == self.course.slug
        )

        self.assertEqual(payload["count"], 2)
        self.assertIn(self.course.slug, slugs)
        self.assertIn(self.other_course.slug, slugs)
        self.assertNotIn(self.draft_course.slug, slugs)
        self.assertEqual(listed_course["student_count"], 1)
        self.assertEqual(listed_course["lesson_count"], 2)
        self.assertEqual(listed_course["thumbnail"], "devops-fundamentals.jpg")

    def test_course_overview_returns_detail_subcomponent_data(self):
        response = self.client.get(
            reverse("course-overview", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], self.course.slug)
        self.assertEqual(response.data["student_count"], 1)
        self.assertEqual(response.data["lesson_count"], 2)
        self.assertEqual(response.data["instructor"]["name"], self.instructor.name)
        self.assertEqual(response.data["category"]["slug"], self.category.slug)
        self.assertEqual(response.data["requirements"], "Basic computer knowledge")

    def test_course_curriculum_returns_sections_and_lessons(self):
        response = self.client.get(
            reverse("course-curriculum", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["description"],
            self.course.curriculum_description,
        )
        self.assertEqual(len(response.data["sections"]), 1)
        section = response.data["sections"][0]
        self.assertEqual(section["title"], self.section.title)
        self.assertEqual([lesson["title"] for lesson in section["lessons"]], [
            "What is DevOps?",
            "Pipeline Basics",
        ])
        self.assertTrue(section["lessons"][0]["is_preview"])
        self.assertFalse(section["lessons"][1]["is_preview"])

    def test_course_instructor_returns_instructor_for_course(self):
        response = self.client.get(
            reverse("course-instructor", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.instructor.name)
        self.assertEqual(response.data["photo"], "ada-photo.jpg")
        self.assertEqual(response.data["thumbnail"], "ada-thumb.jpg")
        self.assertEqual(response.data["specialization"], "DevOps Engineer")

    def test_course_reviews_returns_rating_summary_and_reviews(self):
        response = self.client.get(
            reverse("course-reviews", kwargs={"slug": self.course.slug})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(response.data["total_reviews"], 2)
        self.assertEqual(response.data["rating_distribution"]["5"], 1)
        self.assertEqual(response.data["rating_distribution"]["4"], 1)
        self.assertEqual(len(response.data["reviews"]), 2)

    def test_course_by_category_filters_published_courses(self):
        response = self.client.get(
            reverse("course-by-category"),
            {"category": self.category.slug},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [course["slug"] for course in response.data["payload"]["results"]]
        self.assertEqual(slugs, [self.course.slug])
        self.assertNotIn(self.draft_course.slug, slugs)
        self.assertNotIn(self.other_course.slug, slugs)

    def test_guest_user_can_create_course_comment(self):
        payload = {
            "name": "New Guest",
            "email": "newguest@example.com",
            "message": "The course explained the subject clearly.",
            "rating": 5,
        }

        response = self.client.post(
            reverse("course-comment-create", kwargs={"slug": self.course.slug}),
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])
        self.assertEqual(response.data["message"], payload["message"])
        self.assertTrue(
            Comment.objects.filter(
                course=self.course,
                email=payload["email"],
                rating=payload["rating"],
            ).exists()
        )
