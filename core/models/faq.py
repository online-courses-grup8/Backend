from django.db import models
from django.core.validators import MinLengthValidator


class FAQ(models.Model):
    question = models.TextField(
        validators=[MinLengthValidator(10)]  # soru en az 10 karakter olmalı
    )
    answer = models.TextField(
        validators=[MinLengthValidator(10)]  # cevap en az 10 karakter olmalı
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'FAQs'
        ordering = ['order']