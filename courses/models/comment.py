from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .course import Course

#####COMMENT#######
class Comment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='comments'  # course.comments.all() ile erişilebilir
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments'  # login kullanıcı ise dolu, guest ise null
    )

    name = models.CharField(max_length=100)  # guest kullanıcı için isim
    email = models.EmailField()  # guest kullanıcı için email
    message = models.TextField()  # yorum mesajı
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]  # 0-5 arası olmalı
    )  # puan
    created_at = models.DateTimeField(auto_now_add=True)  # yorum tarihi, otomatik

    def __str__(self):
        return f"{self.name} - {self.course.title}"

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']  # en yeni yorum önce gelir