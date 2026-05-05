from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



####INSTRUCTOR#######
class Instructor(models.Model):
    name = models.CharField(max_length=50)
    bio_hardskill = models.TextField()
    bio_softskill = models.TextField()
    photo = models.ImageField(
        upload_to='assets/img/',
        null=True,
        blank=True
    )
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

