from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


####CARD(SEPET)#####
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'  # user.cart ile erişilebilir
    )
    updated_at = models.DateTimeField(auto_now=True)  # her güncellemede otomatik değişir

    def __str__(self):
        return f"{self.user} - Cart"

    class Meta:
        verbose_name_plural = 'Carts'

#####CARDITEM#####
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'  # cart.items.all() ile erişilebilir
    )
    course = models.ForeignKey(
        'courses.Course',  # string referans, modülerlik korunur
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]  # fiyat negatif olamaz
    )  # sepete eklendiği andaki fiyat
    added_at = models.DateTimeField(auto_now_add=True)  # sepete eklenme tarihi

    def __str__(self):
        return f"{self.cart} - {self.course}"

    class Meta:
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'course']  # aynı kurs sepete iki kez eklenemez


####PAYMENT#####
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
        validators=[MinValueValidator(0.0)]  # tutar negatif olamaz
    )  # toplam ödeme tutarı
    payment_date = models.DateTimeField(auto_now_add=True)  # ödeme tarihi, otomatik
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'  # başlangıçta beklemede
    )  # ödeme durumu
    transaction_id = models.CharField(max_length=200, unique=True)  # tekil işlem id

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']  # en yeni ödeme önce gelir


    ########PAYMENTITEM#########

class PaymentItem(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='items'  # payment.items.all() ile erişilebilir
    )
    course = models.ForeignKey(
        'courses.Course',  # string referans, modülerlik korunur
        on_delete=models.CASCADE,
        related_name='payment_items'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]  # satın alma anındaki fiyat, negatif olamaz
    )

    def __str__(self):
        return f"{self.payment} - {self.course}"

    class Meta:
        verbose_name_plural = 'Payment Items'