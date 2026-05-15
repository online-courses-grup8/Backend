# users/selectors/my_events.py
from events.models import EventRegistration


def get_my_events(user):
    # kullanıcının kayıtlı olduğu etkinlikleri döner
    return EventRegistration.objects.filter(user=user).select_related('event')