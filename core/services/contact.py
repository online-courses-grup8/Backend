from core.models.contact import ContactMessage


def create_contact_message(name, email, message):
    # iletişim formundan gelen mesajı kaydeder
    return ContactMessage.objects.create(
        name=name,
        email=email,
        message=message,
    )