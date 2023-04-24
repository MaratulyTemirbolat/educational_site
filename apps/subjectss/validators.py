from typing import (
    Union,
    Any,
)

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import TemporaryUploadedFile


def validate_negative_class_number(number: int = 0) -> None:
    """Validate class number to be negative."""
    if number < 0:
        raise ValidationError("You cannot set negative number to class")


def validate_vide_format(
    file: Union[TemporaryUploadedFile, Any]
) -> None:
    """Validate the video file."""
    VIDEO_FILE_FORMATS = ("video/mp4",)

    if not isinstance(file, TemporaryUploadedFile):
        raise ValidationError(
            message="Ваш файл должен быть по типу mp4 (video)",
            code="video_file_type_error"
        )
    else:
        if file.content_type not in VIDEO_FILE_FORMATS:
            raise ValidationError(
                message="Расширение файла не по типу видео",
                code="video_file_type_error"
            )
