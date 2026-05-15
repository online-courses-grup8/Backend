# events/services.py
from django.core.exceptions import ValidationError
from events.models import Event, EventRegistration


def register_for_event(user, slug):
    # etkinliği slug ile bul
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        raise ValidationError("Event not found.")

    # zaten kayıtlı mı kontrol et
    if EventRegistration.objects.filter(user=user, event=event).exists():
        raise ValidationError("You are already registered for this event.")

    # kayıt oluştur
    registration = EventRegistration.objects.create(user=user, event=event)
    return registration