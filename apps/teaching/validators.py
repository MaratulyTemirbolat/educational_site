from django.core.exceptions import ValidationError


def validate_teacher_update(teacher: object) -> None:
    """Validate teacher save."""

    if (
        not teacher.subscription and
            (teacher.status_subscription or teacher.datetime_created)):
        raise ValidationError(
            message="Не указали подписку при выборе даты или статуса подписки",
            code="empty_subscription_type_error"
        )
