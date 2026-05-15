from django.contrib.auth.models import AbstractUser
from django.db import models

def user_image_path(instance, filename):
    return filename  # sadece dosya adını döner

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to='assets/img',
        null=True,
        blank=True,
        default='anonymous.jpeg'
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email