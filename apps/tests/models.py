from typing import Any

from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    BooleanField,
    ManyToManyField,
    UniqueConstraint,
    DateTimeField,
    CASCADE,
)

from abstracts.models import AbstractDateTime
from subjectss.models import Topic
from subjectss.models import Student


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
        verbose_name_plural: str = "Ответы"
        verbose_name: str = "Ответ"
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
    QUIZ_MAX_NAME = 250
    name: CharField = CharField(
        max_length=QUIZ_MAX_NAME,
        verbose_name="Название теста"
    )
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
        verbose_name="Вопросы на теста"
    )
    datetime_created: DateTimeField = DateTimeField(
        verbose_name="время и дата создания",
        auto_now_add=True
    )
    attached_questions: ManyToManyField = ManyToManyField(
        to=Question,
        blank=True,
        related_name="quizess",
        verbose_name="Прикрепленные вопросы теста (для чтения)"
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

    class Meta:
        verbose_name: str = "Ответ на вопрос теста"
        verbose_name_plural: str = "Ответы на вопросы тестов"
        constraints: tuple[Any] = (
            UniqueConstraint(
                fields=['quiz', 'question'],
                name="unique_quiz_question"
            ),
        )

    def __str__(self) -> str:
        return f"{self.quiz} {self.question} {self.user_answer}"
