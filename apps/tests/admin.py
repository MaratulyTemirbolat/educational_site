from typing import (
    Union,
    Any,
    Optional,
)

from django.contrib.admin import (
    ModelAdmin,
    register,
)
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from abstracts.admin import AbstractAdminIsDeleted
from tests.filters import CorrectAnswerFilter
from abstracts.filters import DeletedStateFilter
from tests.models import (
    Question,
    Answer,
    Quiz,
    QuizType,
    QuizQuestionAnswer,
)


@register(Question)
class QuestionAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "get_question_short",
        "attached_subject_class",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "get_question_short",
    )
    search_fields: tuple[str] = ("name", "attached_subject_class__name",)
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "attached_subject_class",
                )
            }
        ),
        (
            "Данные состояния",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )
    save_as: bool = True
    save_on_top: bool = True
    list_per_page: int = 25

    def get_question_short(self, obj: Optional[Question] = None) -> str:
        return f"{obj.name[:20]}..."


@register(Answer)
class Answer(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "name",
        "question",
        "is_correct",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "name",
    )
    list_filter: tuple[Any] = (
        DeletedStateFilter,
        "is_correct",
    )
    list_editable: tuple[str] = (
        "is_correct",
    )
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "question",
                    "is_correct",
                )
            }
        ),
        (
            "Данные состояния",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )
    search_fields: tuple[str] = ("name", "question__name",)
    ordering: tuple[str] = ("-datetime_updated", "-id",)
    save_as: bool = True
    save_on_top: bool = True
    list_per_page: int = 20


@register(QuizType)
class QuizTypeAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = ("id", "name", "get_is_deleted_obj",)
    list_display_links: tuple[str] = ("id", "name",)
    list_per_page: int = 10
    search_fields: int = ("name",)
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                )
            }
        ),
        (
            "Данные состояния",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )
    save_as: bool = True
    save_on_top: bool = True
    list_filter: tuple[Any] = (
        DeletedStateFilter,
        "name",
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[QuizType] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("name",)
        return self.readonly_fields


@register(Quiz)
class QuizAdmin(ModelAdmin):
    list_select_related: tuple[str] = (
        "student",
        "quiz_type",
        "student__user",
    )
    list_display: tuple[str] = (
        "id",
        "student",
        "quiz_type",
    )
    list_display_links: tuple[str] = (
        "id",
        "student",
        "quiz_type",
    )
    search_fields: tuple[str] = (
        "student__user__first_name",
        "student__user__last_name",
    )
    list_filter: tuple[str] = ("quiz_type",)
    list_per_page: int = 25
    save_as: bool = True
    save_on_top: bool = True

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[QuizType] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + (
                "student",
                "quiz_type",
            )
        return self.readonly_fields


@register(QuizQuestionAnswer)
class QuizQuestionAnswerAdmin(ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "quiz",
        "get_short_question",
        "user_answer",
        "get_is_correct_answer",
    )
    list_select_related: tuple[str] = (
        "quiz",
        "question",
        "quiz__student",
        "user_answer",
        "quiz__student__user",
        "quiz__quiz_type",
    )
    list_display_links: tuple[str] = (
        "id",
        "quiz",
    )
    list_filter: tuple[Any] = (CorrectAnswerFilter,)
    fields: tuple[str] = (
        "quiz",
        "question",
        "user_answer",
    )
    list_per_page: int = 25

    def __is_correct_answer(
        self,
        obj: Optional[QuizQuestionAnswer] = None
    ) -> bool:
        """Get boolean state of correct asnwer."""
        if obj:
            return obj.answer_point > 0
        return False

    def get_is_correct_answer(
        self,
        obj: Optional[QuizQuestionAnswer] = None
    ) -> str:
        """Get is correct answer."""
        if self.__is_correct_answer(obj=obj):
            return mark_safe(
                '<p style="color:green;font-weight: bold; font-size: 16px;">\
                    Правильный</p>'
            )
        return mark_safe(
            '<p style="color:red;font-weight: bold; font-size: 16px;">\
                Неправильный</p>'
        )
    get_is_correct_answer.short_description = "Правильный ли ответ"

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[QuizQuestionAnswer] = None
    ) -> None:
        """Fill readonly_fields for craeted already obj."""
        if obj:
            return self.readonly_fields + (
                "answer_point",
                "question",
                "user_answer",
                "quiz",
            )
        return self.readonly_fields

    def get_short_question(
        self,
        obj: Optional[QuizQuestionAnswer] = None
    ) -> str:
        """Get short answer of the question."""
        return f"{obj.question.name[:20]}..." if obj else ""
