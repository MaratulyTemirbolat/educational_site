from django.contrib.admin import (
    ModelAdmin,
    register,
)

from abstracts.admin import AbstractAdminIsDeleted
from tests.models import (
    Question,
    Answer,
    Quiz,
    QuizType,
)


@register(Question)
class QuestionAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Answer)
class Answer(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(QuizType)
class QuizTypeAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Quiz)
class SubjectQuizModel(ModelAdmin):
    ...
