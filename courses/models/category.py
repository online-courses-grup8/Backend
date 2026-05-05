from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
#####CATEGORY#####
class Category(models.Model):
    name=models.CharField(max_length=20)
    slug=models.SlugField(unique=True)
    icon = models.ImageField(
        upload_to='assets/img/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

