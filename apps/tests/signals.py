from typing import (
    Any,
    Union,
)
from random import choices

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.base import ModelBase

from tests.models import (
    Question,
    Quiz,
    QuizType,
)
from abstracts.tools import conver_to_int_or_none
from subjectss.models import (
    Topic,
    ClassSubject,
)


@receiver(
    signal=post_save,
    sender=Quiz
)
def post_save_quiz(
    sender: ModelBase,
    instance: Quiz,
    created: bool,
    *args: tuple[Any],
    **kwargs: dict[Any, Any]
) -> None:
    """Add Questions to the model by its quiz_type."""
    quiz_type_id: Union[int, None] = conver_to_int_or_none(
        instance.quiz_type_id
    )
    if created and quiz_type_id == QuizType.TOPIC_QUIZ_TYPE and \
            hasattr(instance, "_topic_id"):
        question_quantity: int = Question.objects.filter(
            attached_subject_class_id=instance._topic_id
        ).count()
        questions: list[Question] = choices(
            Question.objects.filter(attached_subject_class=instance._topic_id),
            k=min(5, question_quantity)
        )
        question: Question
        for question in questions:
            instance.attached_questions.add(question)
    elif created and quiz_type_id == QuizType.CLASS_QUIZ_TYPE and \
            hasattr(instance, "_class_number"):
        class_subject_ids: tuple[int] = tuple(
            ClassSubject.objects.filter(
                attached_class_id=instance._class_number
            ).get_not_deleted().values_list(
                "id",
                flat=True
            )
        )
        topic_ids: tuple[int] = tuple(
            Topic.objects.filter(
                attached_subect_class__in=class_subject_ids
            ).get_not_deleted().values_list(
                "id",
                flat=True
            )
        )
        existed_questions: int = Question.objects.filter(
            attached_subject_class__in=topic_ids
        ).get_not_deleted().count()
        questions: list[Question] = choices(
            Question.objects.filter(
                attached_subject_class__in=topic_ids
            ).get_not_deleted(),
            k=min(10, existed_questions)
        )
        q: Question
        for q in questions:
            instance.attached_questions.add(q)
    elif created and \
        quiz_type_id == QuizType.SUBJECT_QUIZ_TYPE and \
            hasattr(instance, "_subject_id"):
        topic_ids: tuple[int] = tuple(
            Topic.objects.filter(
                attached_subect_class_id=instance._subject_id
            ).get_not_deleted().values_list(
                "id",
                flat=True
            )
        )
        existed_questions: int = Question.objects.filter(
            attached_subject_class__in=topic_ids
        ).get_not_deleted().count()
        questions: list[Question] = choices(
            Question.objects.filter(
                attached_subject_class__in=topic_ids
            ).get_not_deleted(),
            k=min(20, existed_questions)
        )
        q: Question
        for q in questions:
            instance.attached_questions.add(q)
