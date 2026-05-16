# users/services/my_courses.py
from django.utils import timezone
from courses.models.enrollment import Enrollment, LessonProgress


def complete_lesson(enrollment, lesson):
    # dersi tamamlandı olarak işaretler, yoksa oluşturur
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson,
        defaults={
            'is_completed': True,
            'completed_at': timezone.now()
        }
    )
    if not created and not progress.is_completed:
        # daha önce oluşturulmuş ama tamamlanmamışsa güncelle
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
    return progress