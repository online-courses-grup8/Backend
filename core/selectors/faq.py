from core.models.faq import FAQ


def get_active_faqs():
    # sadece aktif FAQ'ları sıralı getirir
    return FAQ.objects.filter(is_active=True)