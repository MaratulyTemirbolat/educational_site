from typing import Any

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.base import ModelBase

from auths.models import CustomUser
from teaching.models import Teacher
from subjectss.models import Student


@receiver(
    signal=post_save,
    sender=CustomUser
)
def post_save_quiz(
    sender: ModelBase,
    instance: CustomUser,
    created: bool,
    *args: tuple[Any],
    **kwargs: dict[Any, Any]
) -> None:
    """Add Questions to the model by its quiz_type."""
    if created and \
        hasattr(instance, "_is_student") and \
            not Student.objects.filter(user_id=instance.id).exists():
        Student.objects.create(user=instance)
    if created and \
        hasattr(instance, "_is_teacher") and \
            not Teacher.objects.filter(user_id=instance.id).exists():
        Teacher.objects.create(user=instance)
