from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinLengthValidator

####TAG###
class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]  # tag adı en az 2 karakter
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tags'

#####BLOGPOST####
class BlogPost(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)]  # başlık en az 5 karakter
    )
    slug = models.SlugField(unique=True)  # URL için tekil isim, otomatik validasyon var
    content = models.TextField(
        validators=[MinLengthValidator(50)]  # içerik en az 50 karakter
    )
    thumbnail = models.ImageField(upload_to='blog/', null=True, blank=True)  # blog görseli, opsiyonel
    category = models.CharField(max_length=100)  # blog kategorisi
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'  # user.blog_posts.all() ile erişilebilir
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'  # tag.posts.all() ile erişilebilir
    )
    is_published = models.BooleanField(default=False)  # yayında mı
    created_at = models.DateTimeField(auto_now_add=True)  # oluşturulma tarihi, otomatik

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Blog Posts'
        ordering = ['-created_at']  # en yeni blog önce gelir