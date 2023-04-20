from django.core.exceptions import ValidationError


def validate_negative_class_number(number: int = 0) -> None:
    if number < 0:
        raise ValidationError("You cannot set negative number to class")
