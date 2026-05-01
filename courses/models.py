from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

#####CATEGORY#####
class Category(models.Model):
    name=models.CharField(max_length=20)
    slug=models.SlugField(unique=True)
    icon=models.ImageField(upload_to='categories/',null=True,blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'



####INSTRUCTOR#######
class Instructor(models.Model):
    name = models.CharField(max_length=50)
    bio_hardskill = models.TextField()
    bio_softskill = models.TextField()
    photo = models.ImageField(upload_to='instructors/', null=True, blank=True)
    specialization = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    experience = models.IntegerField(default=0)
    position = models.CharField(max_length=50,default="Teacher")
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Instructors'

class InstructorSkill(models.Model):
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill = models.CharField(max_length=200)
    percentage = models.IntegerField(
        default=0, # skill yetkinlik yüzdesi
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.instructor.name} - {self.skill}"



####COURSE######
class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # URL için tekil isim, otomatik validasyon var
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/')  # pillow format kontrolü yapar
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


#######COURSE_SECTION##########
class CourseSection(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'  # course.sections.all() ile erişilebilir
    )
    title = models.CharField(max_length=200)
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