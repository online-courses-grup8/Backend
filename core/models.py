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


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]  # isim en az 2 karakter olmalı
    )
    email = models.EmailField()  # email formatı otomatik kontrol ediliyor
    message = models.TextField(
        validators=[MinLengthValidator(10)]  # mesaj en az 10 karakter olmalı
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')  # pillow format kontrolü yapıyor
    caption = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

    class Meta:
        verbose_name_plural = 'Gallery Images'
        ordering = ['-uploaded_at']