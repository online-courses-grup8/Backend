from django.urls import path
from core.views.faq import FAQListView
from core.views.contact import ContactMessageCreateView
from core.views.newsletter import NewsletterSubscribeView
from core.views.stats import SiteStatsView

urlpatterns = [
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    # POST /api/v1/newsletter/ email kaydeder
    path('newsletter/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    # GET /api/v1/stats/ - site istatistiklerini döner
    path('stats/', SiteStatsView.as_view(), name='site-stats'),
]