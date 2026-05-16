from django.test import SimpleTestCase  # Veritabanı gerekmediği için daha hızlı
from unittest.mock import MagicMock
from blog.serializers import BlogListSerializer


class BlogListSerializerTest(SimpleTestCase):

    def setUp(self):
        # Her testten önce serializer nesnesini bir kez oluşturuyoruz
        self.serializer = BlogListSerializer()

    def _make_post(self, thumbnail_path=None, author_photo_path=None):
        """
        Mock BlogPost objesi oluşturur.
        Tam path verilmesine imkan tanıyarak farklı senaryoları test etmemizi sağlar.
        """
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

    # --- Thumbnail Testleri ---

    def test_thumbnail_returns_filename_when_exists(self):
        # Standart durum: assets/img/test.jpg -> test.jpg
        post = self._make_post(thumbnail_path="assets/img/photo.jpg")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "photo.jpg")

    def test_thumbnail_returns_filename_with_extra_dots(self):
        # Uç durum: Dosya adında birden fazla nokta varsa (örn: my.trip.v1.png)
        post = self._make_post(thumbnail_path="assets/img/my.trip.v1.png")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "my.trip.v1.png")

    def test_thumbnail_returns_none_when_missing(self):
        # Dosya yoksa None dönmeli
        post = self._make_post()
        result = self.serializer.get_thumbnail(post)
        self.assertIsNone(result)

    # --- Author Photo Testleri ---

    def test_author_photo_returns_filename_when_exists(self):
        # Standart durum: blog/authors/johndoe.png -> johndoe.png
        post = self._make_post(author_photo_path="blog/authors/johndoe.png")
        result = self.serializer.get_author_photo(post)
        self.assertEqual(result, "johndoe.png")

    def test_author_photo_returns_none_when_missing(self):
        # Dosya yoksa None dönmeli
        post = self._make_post()
        result = self.serializer.get_author_photo(post)
        self.assertIsNone(result)

    # --- Ekstra Sağlamlık Testi (Edge Case) ---

    def test_returns_original_if_no_slash_in_path(self):
        # Eğer path içinde hiç '/' yoksa direkt kendisini mi döndürüyor?
        # (os.path.basename kullanıyorsan bu test başarıyla geçer)
        post = self._make_post(thumbnail_path="direct_file.jpg")
        result = self.serializer.get_thumbnail(post)
        self.assertEqual(result, "direct_file.jpg")