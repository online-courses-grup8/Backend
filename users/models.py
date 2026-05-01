from django.contrib.auth.models import AbstractUser
from django.db import models



######USER########
class User(AbstractUser):
    email = models.EmailField(unique=True)  # email unique olmalı
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'  # email ile login
    REQUIRED_FIELDS = ['username']  # zorunlu alanlar

    def __str__(self):
        return self.email