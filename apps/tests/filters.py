from typing import Optional

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin import ModelAdmin

from tests.models import QuizQuestionAnswer


class CorrectAnswerFilter(SimpleListFilter):
    """IsCorrectAnswerFilter."""

    title: str = "Правильность ответов"
    parameter_name: str = "answers"

    def lookups(
        self,
        request: WSGIRequest,
        model_admin: ModelAdmin
    ) -> list[tuple[str, str]]:
        """Return tuple of value and verbose value."""
        return [
            ("correct", "Правильные ответы"),
            ("wrong", "Неправильные ответы"),
        ]

    def queryset(
        self,
        request: WSGIRequest,
        queryset: QuerySet[QuizQuestionAnswer]
    ) -> Optional[QuerySet[QuizQuestionAnswer]]:
        """Return queryset by value."""
        if self.value() == "correct":
            return queryset.filter(answer_point__gt=0)
        if self.value() == "wrong":
            return queryset.filter(answer_point=0)
