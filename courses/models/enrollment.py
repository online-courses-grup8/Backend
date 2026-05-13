from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .course import Course
from .curriculum import CourseLesson

#####Enrollment####
class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # settings'de tanımlı custom User modelini kullanır
        on_delete=models.CASCADE,
        related_name='enrollments'  # user.enrollments.all() ile erişilebilir
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'  # course.enrollments.all() ile erişilebilir
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)  # kayıt tarihi, otomatik

    def __str__(self):
        return f"{self.user} - {self.course.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # yeni kayıt mı
        super().save(*args, **kwargs)
        if is_new:
            # yeni enrollment oluşunca student_count artır
            Course.objects.filter(pk=self.course.pk).update(
                student_count=models.F('student_count') + 1
            )
    class Meta:
        verbose_name_plural = 'Enrollments'
        unique_together = ['user', 'course']  # aynı kullanıcı aynı kursa iki kez kayıt olamaz



######LESSONPROGRESS######
class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='progress'  # enrollment.progress.all() ile erişilebilir
    )
    lesson = models.ForeignKey(
        CourseLesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    is_completed = models.BooleanField(default=False)  # ders tamamlandı mı
    watched_duration = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]  # negatif olamaz, saniye cinsinden
    )  #ne kadar izlendi
    completed_at = models.DateTimeField(null=True, blank=True)  # tamamlanma tarihi, opsiyonel

    def __str__(self):
        return f"{self.enrollment} - {self.lesson.title}"

    class Meta:
        verbose_name_plural = 'Lesson Progress'
        unique_together = ['enrollment', 'lesson']  # aynı enrollment + lesson bir kez olabilir

