from django.core.exceptions import ValidationError


def validate_questions_number(points: int) -> None:
    if points < 0:
        raise ValidationError(
            message="Количество правильных ответов не может быть отрицательны",
            code="negative_points_error"
        )


def validate_negative_point(points: int) -> None:
    if points < 0:
        raise ValidationError(
            message="Балл за вопрос не должен быть отрицательным",
            code="negative_answer_point"
        )
