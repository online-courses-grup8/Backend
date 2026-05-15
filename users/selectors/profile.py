# users/selectors/profile.py
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()


def get_user_profile(user):
    # enrollment ve payment sayılarını tek sorguda annotate ile getirir
    return User.objects.annotate(
        enrollment_count=Count('enrollments', distinct=True),
        payment_count=Count('payments', distinct=True),
    ).get(pk=user.pk)