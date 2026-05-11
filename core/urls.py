from django.urls import path
from core.views.faq import FAQListView
from core.views.contact import ContactMessageCreateView

urlpatterns = [
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
]