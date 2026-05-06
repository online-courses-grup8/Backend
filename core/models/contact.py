from django.db import models
from django.core.validators import MinLengthValidator


class ContactMessage(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    email = models.EmailField()
    message = models.TextField(
        validators=[MinLengthValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']