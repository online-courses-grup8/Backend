from core.models.newsletter import NewsletterSubscriber


def subscribe_newsletter(email):
    # emaili newsletter listesine kaydeder
    return NewsletterSubscriber.objects.create(email=email)