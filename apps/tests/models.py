from typing import Any

from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    BooleanField,
    ManyToManyField,
    UniqueConstraint,
    IntegerField,
    CASCADE,
)

from abstracts.models import AbstractDateTime
from subjectss.models import Topic
from subjectss.models import Student
from tests.validators import (
    validate_questions_number,
    validate_negative_point,
)


class QuizType(AbstractDateTime):
    QUIZ_NAME_LIMIT = 100
    name: CharField = CharField(
        max_length=QUIZ_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование типа теста"
    )

    class Meta:
        verbose_name: str = "Тип теста"
        verbose_name_plural: str = "Типы тестов"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return self.name


class Question(AbstractDateTime):
    TEST_NAME_LIMIT = 240
    name: CharField = CharField(
        max_length=TEST_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )
    attached_subject_class: Topic = ForeignKey(
        to=Topic,
        on_delete=CASCADE,
        related_name="questions",
        verbose_name="Вопрос к теме"
    )

    class Meta:
        verbose_name_plural: str = "Вопросы"
        verbose_name: str = "Вопрос"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return self.name


class Answer(AbstractDateTime):
    ANSWER_NAME_LIMIT = 250
    name: CharField = CharField(
        max_length=ANSWER_NAME_LIMIT,
        verbose_name="Ответ"
    )
    question: Question = ForeignKey(
        to=Question,
        on_delete=CASCADE,
        related_name="answers",
        verbose_name="Ответ к вопросу"
    )
    is_correct: BooleanField = BooleanField(
        default=False,
        verbose_name="Правильный ответ?"
    )

    class Meta:
        verbose_name_plural: str = "Возможные ответы на вопросы"
        verbose_name: str = "Возможный ответ на вопрос"
        ordering: tuple[str] = ("-datetime_updated",)
        constraints: tuple[Any] = (
            UniqueConstraint(
                fields=['name', 'question'],
                name="unique_asnwer_name_question"
            ),
        )

    def __str__(self) -> str:
        return self.name


class Quiz(Model):
    student: Student = ForeignKey(
        to=Student,
        on_delete=CASCADE,
        related_name="subject_quizes",
        verbose_name="Зарегестрированный стедент"
    )
    quiz_type: QuizType = ForeignKey(
        to=QuizType,
        on_delete=CASCADE,
        related_name="quizes",
        verbose_name="Тип куиза"
    )
    questions: ManyToManyField = ManyToManyField(
        to=Question,
        through="QuizQuestionAnswer",
        through_fields=["quiz", "question"],
        verbose_name="Вопросы на предмет"
    )
    correct_answers: IntegerField = IntegerField(
        default=0,
        validators=(validate_questions_number,),
        verbose_name="Количество правильных ответов"
    )

    class Meta:
        verbose_name: str = "Тест"
        verbose_name_plural: str = "Тесты"

    def __str__(self) -> str:
        return f"Студент: '{self.student}' Тип теста: '{self.quiz_type}'"


class QuizQuestionAnswer(Model):
    quiz: Quiz = ForeignKey(
        to=Quiz,
        on_delete=CASCADE,
        related_name="quiz_questions",
        verbose_name="Тест"
    )
    question: Question = ForeignKey(
        to=Question,
        on_delete=CASCADE,
        related_name="quiz_questions",
        verbose_name="Вопрос"
    )
    user_answer: Answer = ForeignKey(
        to=Answer,
        on_delete=CASCADE,
        related_name="user_answer",
        verbose_name="Ответ пользователя"
    )
    answer_point: IntegerField = IntegerField(
        default=0,
        validators=[validate_negative_point],
        verbose_name="Баллы за ответ"
    )

    class Meta:
        verbose_name: str = "Ответ на вопрос теста"
        verbose_name_plural: str = "Ответы на вопросы тестов"

    def __str__(self) -> str:
        return f"{self.quiz} {self.question} {self.user_answer}"
