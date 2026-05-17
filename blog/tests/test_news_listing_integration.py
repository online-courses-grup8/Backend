"""
Test Case #270 / Task #270 - News module listing integration tests
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/270

Goal:
Verify backend integration coverage for the currently available Blog/News list
endpoint so readers can access published posts reliably.

Flow:
1. Create published and unpublished blog/news records in the test database
2. Request the public blog listing endpoint
3. Verify only published posts are returned
4. Verify results are ordered by newest created_at value first
5. Verify image fields are serialized as filenames
6. Verify pagination metadata and limit query parameter work correctly
"""

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import BlogPost


class NewsListingIntegrationTest(APITestCase):
    def setUp(self):
        self.blog_list_url = reverse("blog-list")

    def _create_post(
        self,
        title,
        slug,
        *,
        is_published=True,
        created_at=None,
        thumbnail="asset/img/news-thumbnail.jpg",
        author_photo="blog/authors/author-photo.jpg",
    ):
        post = BlogPost.objects.create(
            title=title,
            slug=slug,
            content=(
                "This is a long enough news article body used for integration "
                "testing of the news listing API response."
            ),
            thumbnail=thumbnail,
            category="Education",
            author_name="Jane Doe",
            author_photo=author_photo,
            author_position="Editor",
            is_published=is_published,
        )
        if created_at:
            BlogPost.objects.filter(pk=post.pk).update(created_at=created_at)
            post.refresh_from_db()
        return post

    def test_blog_list_returns_only_published_posts_with_serialized_image_filenames(self):
        older_post = self._create_post(
            "Older Published News",
            "older-published-news",
            created_at=timezone.datetime(2026, 5, 10, tzinfo=timezone.get_current_timezone()),
            thumbnail="asset/img/older-thumb.jpg",
            author_photo="blog/authors/older-author.png",
        )
        newest_post = self._create_post(
            "Newest Published News",
            "newest-published-news",
            created_at=timezone.datetime(2026, 5, 12, tzinfo=timezone.get_current_timezone()),
            thumbnail="asset/img/newest-thumb.jpg",
            author_photo="blog/authors/newest-author.png",
        )
        self._create_post(
            "Draft News Hidden",
            "draft-news-hidden",
            is_published=False,
            created_at=timezone.datetime(2026, 5, 13, tzinfo=timezone.get_current_timezone()),
        )

        response = self.client.get(self.blog_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 200)
        self.assertIsNone(response.data["errorMessage"])
        self.assertEqual(response.data["payload"]["count"], 2)

        results = response.data["payload"]["results"]
        self.assertEqual([item["id"] for item in results], [newest_post.id, older_post.id])
        self.assertEqual([item["slug"] for item in results], [newest_post.slug, older_post.slug])
        self.assertEqual(results[0]["thumbnail"], "newest-thumb.jpg")
        self.assertEqual(results[0]["author_photo"], "newest-author.png")
        self.assertEqual(results[1]["thumbnail"], "older-thumb.jpg")
        self.assertEqual(results[1]["author_photo"], "older-author.png")
        self.assertNotIn("draft-news-hidden", [item["slug"] for item in results])

    def test_blog_list_supports_limit_pagination(self):
        for index in range(3):
            self._create_post(
                title=f"Published News {index}",
                slug=f"published-news-{index}",
                created_at=timezone.datetime(
                    2026,
                    5,
                    10 + index,
                    tzinfo=timezone.get_current_timezone(),
                ),
            )

        response = self.client.get(self.blog_list_url, {"limit": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = response.data["payload"]

        self.assertEqual(payload["count"], 3)
        self.assertIsNotNone(payload["next"])
        self.assertIsNone(payload["previous"])
        self.assertEqual(len(payload["results"]), 2)
        self.assertEqual(
            [item["slug"] for item in payload["results"]],
            ["published-news-2", "published-news-1"],
        )

    def test_blog_list_returns_empty_payload_when_no_news_is_published(self):
        self._create_post(
            "Draft News Hidden",
            "draft-news-hidden",
            is_published=False,
        )

        response = self.client.get(self.blog_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["count"], 0)
        self.assertEqual(response.data["payload"]["results"], [])
