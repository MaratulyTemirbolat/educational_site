from django.core.exceptions import ValidationError


def validate_negative_int(value: int = 0):
    if value < 0:
        raise ValidationError(
            message="You cannot assign negative value",
            code="neg_value_error"
        )
