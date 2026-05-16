from django.shortcuts import get_object_or_404
from events.models import Event


def get_all_events():
    #Tüm etkinlikleri tarihe göre sıralı döner."""
    return Event.objects.all()


def get_event_by_slug(slug):
    #Slug'a göre tek etkinlik döner, bulunamazsa 404 fırlatır."""
    return get_object_or_404(Event, slug=slug)

def get_home_events():
    # ana sayfa icin yaklasan etkinlikleri tarihe gore sirali doner
    return Event.objects.order_by('date')