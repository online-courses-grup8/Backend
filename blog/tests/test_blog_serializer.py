"""
Test Case #272 / Task #272 - News module unit test review
Azure DevOps Work Item: https://dev.azure.com/grup8devops/Online_Course/_workitems/edit/272

Goal:
Review and keep unit test coverage for the news/blog serializer helpers that
format image fields for API responses.

Flow:
1. Verify thumbnail path values are returned as filenames
2. Verify missing thumbnail values return None
3. Verify author photo path values are returned as filenames
4. Verify missing author photo values return None
5. Verify direct filenames without folders are preserved
"""

from django.test import SimpleTestCase
from unittest.mock import MagicMock

from blog.serializers import BlogListSerializer


class BlogListSerializerTest(SimpleTestCase):

    def setUp(self):
        self.serializer = BlogListSerializer()

    def _make_post(self, thumbnail_path=None, author_photo_path=None):
        post = MagicMock()

        if thumbnail_path:
            thumbnail = MagicMock()
            thumbnail.name = thumbnail_path
            post.thumbnail = thumbnail
        else:
            post.thumbnail = None

        if author_photo_path:
            author_photo = MagicMock()
            author_photo.name = author_photo_path
            post.author_photo = author_photo
        else:
            post.author_photo = None

        return post

    def test_thumbnail_returns_filename_when_exists(self):
        post = self._make_post(thumbnail_path="assets/img/photo.jpg")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "photo.jpg")

    def test_thumbnail_returns_filename_with_extra_dots(self):
        post = self._make_post(thumbnail_path="assets/img/my.trip.v1.png")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "my.trip.v1.png")

    def test_thumbnail_returns_none_when_missing(self):
        post = self._make_post()
        result = self.serializer.get_thumbnail(post)
        self.assertIsNone(result)

    def test_author_photo_returns_filename_when_exists(self):
        post = self._make_post(author_photo_path="blog/authors/johndoe.png")
        result = self.serializer.get_author_photo(post)
        self.assertEqual(result, "johndoe.png")

    def test_author_photo_returns_none_when_missing(self):
        post = self._make_post()
        result = self.serializer.get_author_photo(post)
        self.assertIsNone(result)

    def test_returns_original_if_no_slash_in_path(self):
        post = self._make_post(thumbnail_path="direct_file.jpg")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "direct_file.jpg")
