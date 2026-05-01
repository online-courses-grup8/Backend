from django.db import models
from django.core.validators import MinValueValidator

class Event(models.Model):
    title = models.CharField(max_length=200)  # etkinlik adı
    slug = models.SlugField(unique=True)  # URL için tekil isim
    description = models.TextField()  # etkinlik açıklaması
    date = models.DateTimeField()  # etkinlik tarihi
    start_time = models.TimeField()  # başlangıç saati
    end_time = models.TimeField()  # bitiş saati
    location = models.CharField(max_length=200)  # mekan adı
    is_online = models.BooleanField(default=False)  # online mı yüz yüze mi
    language = models.CharField(max_length=50)  # etkinlik dili
    phone = models.CharField(max_length=20, null=True, blank=True)  # iletişim telefonu, opsiyonel
    email = models.EmailField(null=True, blank=True)  # iletişim emaili, opsiyonel
    image = models.ImageField(upload_to='events/', null=True, blank=True)  # etkinlik görseli, opsiyonel
    facebook = models.URLField(null=True, blank=True)  # facebook linki
    instagram = models.URLField(null=True, blank=True)  # instagram linki
    linkedin = models.URLField(null=True, blank=True)  # linkedin linki
    twitter = models.URLField(null=True, blank=True)  # twitter linki

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        # bitiş saati başlangıç saatinden önce olamaz
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("Bitiş saati başlangıç saatinden sonra olmalı.")
        # geçmiş tarihe etkinlik eklenemez
        from django.utils import timezone
        if self.date and self.date < timezone.now():
            raise ValidationError("Etkinlik tarihi geçmişte olamaz.")

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ['-date']  # en yeni etkinlik önce gelir