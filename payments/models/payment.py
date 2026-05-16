# payments/models/payment.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid
from decimal import Decimal


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),      # beklemede
        ('completed', 'Completed'),  # tamamlandı
        ('failed', 'Failed'),        # başarısız
        ('refunded', 'Refunded'),    # iade edildi
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'  # user.payments.all() ile erişilebilir
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]  # tutar negatif olamaz
    )  # toplam ödeme tutarı
    payment_date = models.DateTimeField(auto_now_add=True)  # ödeme tarihi, otomatik
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'  # başlangıçta beklemede
    )
    card_last_four = models.CharField(max_length=4)  # son 4 hane
    transaction_id = models.CharField(max_length=200, unique=True)  # tekil işlem id

    def save(self, *args, **kwargs):
        # transaction id otomatik üret
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']


class PaymentItem(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='items'  # payment.items.all() ile erişilebilir
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='payment_items'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]  # satın alma anındaki fiyat
    )

    def __str__(self):
        return f"{self.payment} - {self.course}"

    class Meta:
        verbose_name_plural = 'Payment Items'