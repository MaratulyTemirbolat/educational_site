from django.core.exceptions import ValidationError


def validate_questions_number(points: int) -> None:
    if points < 0:
        raise ValidationError(
            message="Количество правильных ответов не может быть отрицательным",
            code="negative_points_error"
        )
