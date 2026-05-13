# payments/services/cart.py
from django.core.exceptions import ValidationError
from courses.models import Course
from courses.models.enrollment import Enrollment
from payments.models import CartItem
from payments.selectors.cart import get_or_create_cart, is_course_in_cart


def add_to_cart(user, course_id):
    """
    Kursu kullanıcının sepetine ekler.
    - Kurs bulunamazsa hata fırlatır
    - Zaten satın alınmışsa hata fırlatır
    - Zaten sepetteyse hata fırlatır
    - Başarılıysa CartItem döner
    """
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise ValidationError("Course not found.")

    # kurs zaten satın alınmış mı
    if Enrollment.objects.filter(user=user, course=course).exists():
        raise ValidationError("You already own this course.")

    # kurs zaten sepette mi
    if is_course_in_cart(user, course):
        raise ValidationError("Course is already in your cart.")

    cart = get_or_create_cart(user)
    # o anki fiyat snapshot'ı alınır, ileride fiyat değişse bile etkilenmez
    item = CartItem.objects.create(
        cart=cart,
        course=course,
        price=course.price
    )
    return item


def remove_from_cart(user, item_id):
    """
    Sepetten kurs kaldırır.
    - item_id ile CartItem bulunur
    - Bulunamazsa hata fırlatır
    """
    cart = get_or_create_cart(user)
    try:
        item = cart.items.get(id=item_id)
    except CartItem.DoesNotExist:
        raise ValidationError("Cart item not found.")
    item.delete()


def sync_cart(user, course_ids):
    """
    Login olduktan sonra local storage'daki kursları backend sepetine aktarır.
    Her kurs için add_to_cart çağrılır:
    - Başarılıysa added listesine eklenir
    - Zaten satın alınmışsa already_owned listesine eklenir
    - Zaten sepetteyse already_in_cart listesine eklenir
    Frontend bu listeye göre kullanıcıya bilgi verir.
    """
    added = []
    already_owned = []
    already_in_cart = []

    for course_id in course_ids:
        try:
            add_to_cart(user, course_id)
            added.append(course_id)
        except ValidationError as e:
            message = str(e.message)
            if "already own" in message:
                already_owned.append(course_id)
            elif "already in your cart" in message:
                already_in_cart.append(course_id)

    return {
        "added": added,
        "already_owned": already_owned,
        "already_in_cart": already_in_cart,
    }