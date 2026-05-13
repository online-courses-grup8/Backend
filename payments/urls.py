# payments/urls.py
from django.urls import path
from payments.views.cart import CartView, CartAddView, CartRemoveView, CartSyncView

urlpatterns = [
    # GET /api/v1/cart/ → sepeti getir
    path('cart/', CartView.as_view(), name='cart'),
    # POST /api/v1/cart/add/ → sepete kurs ekle
    path('cart/add/', CartAddView.as_view(), name='cart-add'),
    # DELETE /api/v1/cart/remove/<item_id>/ → sepetten kurs kaldır
    path('cart/remove/<int:item_id>/', CartRemoveView.as_view(), name='cart-remove'),
    # POST /api/v1/cart/sync/ → local storage'dan senkronize et
    path('cart/sync/', CartSyncView.as_view(), name='cart-sync'),
]