from events.models import Event


def get_all_events():
    # tüm etkinlikleri tarihe göre sıralı getirir
    return Event.objects.all()