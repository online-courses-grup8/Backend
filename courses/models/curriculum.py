from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from .course import Course

#######COURSE_SECTION##########
class CourseSection(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'  # course.sections.all() ile erişilebilir
    )
    title = models.CharField(max_length=200)
    description = models.TextField(
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(10),  # en az 10 karakter
            MaxLengthValidator(200)
        ]
    )
    order = models.IntegerField(default=0)  # sıralama için

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name_plural = 'Course Sections'
        ordering = ['order']  # otomatik sıralı gelir



#######COURSE_LESSON######
class CourseLesson(models.Model):
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='lessons'  # section.lessons.all() ile erişilebilir
    )
    title = models.CharField(max_length=200)  # ders adı

    duration = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]  # süre negatif olamaz, dakika cinsinden
    )
    order = models.IntegerField(default=0)  # sıralama için
    is_free = models.BooleanField(default=False)  # ücretsiz önizleme var mı
    is_previewed = models.BooleanField(default=False)  # izlenmiş mi (genel önizleme)

    def __str__(self):
        return f"{self.section.title} - {self.title}"

    class Meta:
        verbose_name_plural = 'Course Lessons'
        ordering = ['order']  # otomatik sıralı gelir
