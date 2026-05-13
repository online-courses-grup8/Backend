# payments/selectors/cart.py
from payments.models import Cart, CartItem


def get_or_create_cart(user):
    # kullanıcının sepetini getirir, yoksa oluşturur
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def get_cart_items(user):
    # kullanıcının sepetindeki tüm kursları getirir
    cart = get_or_create_cart(user)
    return cart.items.select_related('course').all()


def get_cart_total(user):
    # sepetteki toplam tutarı hesaplar
    items = get_cart_items(user)
    return sum(item.price for item in items)


def is_course_in_cart(user, course):
    # kurs sepette var mı kontrol eder
    cart = get_or_create_cart(user)
    return cart.items.filter(course=course).exists()