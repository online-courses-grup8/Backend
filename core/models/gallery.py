from django.db import models


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

    class Meta:
        verbose_name_plural = 'Gallery Images'
        ordering = ['-uploaded_at']