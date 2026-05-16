from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)  # etkinlik adı
    slug = models.SlugField(unique=True)  # URL için tekil isim
    description = models.TextField()  # etkinlik açıklaması
    requirements = models.TextField(null=True, blank=True)
    requirements_list = models.JSONField(default=list, blank=True)  # tikli madde madde liste
    date = models.DateTimeField()  # etkinlik tarihi
    start_time = models.TimeField()  # başlangıç saati
    end_time = models.TimeField()  # bitiş saati
    location = models.CharField(max_length=200)  # mekan adı
    hall_number = models.CharField(max_length=50, null=True, blank=True)  # Hall No: 59
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # harita için
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # harita için
    is_online = models.BooleanField(default=False)  # online mı yüz yüze mi
    category = models.CharField(max_length=100, null=True, blank=True)  # etkinlik kategorisi, örn: Skills, Programming
    language = models.CharField(max_length=50)  # etkinlik dili
    phone = models.CharField(max_length=20, null=True, blank=True)  # iletişim telefonu, opsiyonel
    email = models.EmailField(null=True, blank=True)  # iletişim emaili, opsiyonel
    image = models.ImageField( upload_to='assets/img/', null=True, blank=True)  # etkinlik görseli, opsiyonel
    image2 = models.ImageField( upload_to='assets/img/', null=True, blank=True)  # etkinlik görseli, opsiyonel
    image3 = models.ImageField( upload_to='assets/img/', null=True, blank=True)  # etkinlik görseli, opsiyonel

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        # bitiş saati başlangıç saatinden önce olamaz
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("Bitiş saati başlangıç saatinden sonra olmalı.")
        # geçmiş tarihe etkinlik eklenemez
        if self.date and self.date < timezone.now():
            raise ValidationError("Etkinlik tarihi geçmişte olamaz.")

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ['-date']  # en yeni etkinlik önce gelir





class EventRegistration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'event']  # aynı kullanıcı aynı etkinliğe iki kez kayıt olamaz
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"