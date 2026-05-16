from django.db import models


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)  # aynı email iki kez eklenemez
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Newsletter Subscribers'