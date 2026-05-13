from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Cart(models.Model):
    # kullanıcının aktif sepeti, her kullanıcının bir sepeti olur
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - Cart"

    class Meta:
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    # sepetteki her bir kurs kalemi
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    course = models.ForeignKey(
        'courses.Course',  # string referans, modülerlik korunur
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )  # eklenme anındaki fiyat snapshot'ı
    added_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # fiyat negatif olamaz
        if self.price is not None and self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'course']  # aynı kurs iki kez eklenemez

    def __str__(self):
        return f"{self.cart.user.email} - {self.course.title}"