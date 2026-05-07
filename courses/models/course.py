from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .category import Category
from .instructor import Instructor

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # URL için tekil isim, otomatik validasyon var
    description = models.TextField()
    requirements = models.TextField(null=True, blank=True)  # kurs gereksinimleri
    thumbnail = models.ImageField(
        upload_to='assets/img/'
    ) # pillow format kontrolü yapar
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]  #kurs negatif olamaz
    )
    duration = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]  # süre negatif olamaz
    )  # toplam süre dakika cinsinden
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)  # beginner, intermediate, expert
    language = models.CharField(max_length=50)
    certification = models.BooleanField(default=False)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]  # 0-5 arası olmalı
    )  # ortalama puan
    video_url = models.URLField(null=True, blank=True)
    is_published = models.BooleanField(default=False)  # yayında mı
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'  # category.courses.all() ile erişilebilir
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses'  # instructor.courses.all() ile erişilebilir
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']  # en yeni kurs önce gelir
