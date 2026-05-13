from django.db import transaction
from django.core.exceptions import ValidationError
from courses.models.enrollment import Enrollment
from payments.models import Payment, PaymentItem
from payments.selectors.cart import get_or_create_cart, get_cart_total


def process_checkout(user, card_last_four):
    """
    Ödeme işlemini gerçekleştirir:
    1. Sepet boş mu kontrol eder
    2. Payment oluşturur
    3. Her CartItem için PaymentItem oluşturur
    4. Her kurs için Enrollment oluşturur
    5. Payment status'ü completed yapar
    6. Sepeti temizler
    Tüm işlemler transaction içinde yapılır, hata olursa geri alınır.
    """
    cart = get_or_create_cart(user)
    items = cart.items.select_related('course').all()

    # sepet boş mu kontrol et
    if not items.exists():
        raise ValidationError("Your cart is empty.")

    total = get_cart_total(user)

    with transaction.atomic():
        # payment oluştur
        payment = Payment.objects.create(
            user=user,
            amount=total,
            status='pending',
            card_last_four=card_last_four,
        )

        enrolled_courses = []

        for item in items:
            # her kurs için payment item oluştur
            PaymentItem.objects.create(
                payment=payment,
                course=item.course,
                price=item.price,
            )

            # her kurs için enrollment oluştur
            Enrollment.objects.get_or_create(
                user=user,
                course=item.course,
            )

            enrolled_courses.append(item.course.id)

        # ödeme tamamlandı
        payment.status = 'completed'
        payment.save()

        # sepeti temizle
        cart.items.all().delete()

    return payment, enrolled_courses