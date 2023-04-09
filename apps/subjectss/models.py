from typing import Any

from django.db.models import (
    CharField,
    IntegerField,
    ManyToManyField,
    Model,
    UniqueConstraint,
    CASCADE,
    ForeignKey,
)

from apps.abstracts.models import AbstractDateTime
from apps.subjectss.validators import validate_negative_class_number


class Topic(AbstractDateTime):
    TOPIC_NAME_LIMIT = 240
    name: CharField = CharField(
        max_length=TOPIC_NAME_LIMIT,
        verbose_name="Название"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Тема предмета"
        verbose_name_plural: str = "Темы предметов"

    def __str__(self) -> str:
        return self.name


class Class(AbstractDateTime):
    number: IntegerField = IntegerField(
        unique=True,
        db_index=True,
        validators=[validate_negative_class_number],
        verbose_name="Номер класса"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Класс"
        verbose_name_plural: str = "Классы"

    def __str__(self) -> str:
        return f"{self.number} класс"


class Subject(AbstractDateTime):
    SUBJECT_NAME_LIMIT = 200

    name: CharField = CharField(
        max_length=SUBJECT_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )
    classes: ManyToManyField = ManyToManyField(
        to=Class,
        through="SubjectClassTopic",
        through_fields=("subject", "class_number"),
        related_name="subject_classes",
        verbose_name="Классы"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Предмет"
        verbose_name_plural: str = "Предметы"

    def __str__(self) -> str:
        return self.name


class TrackWay(AbstractDateTime):
    TRACKWAY_NAME_LIMIT = 200

    name: CharField = CharField(
        max_length=TRACKWAY_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование трэка"
    )
    subjects: ManyToManyField = ManyToManyField(
        to=Subject,
        blank=True,
        related_name="tracks",
        verbose_name="Предметы по направлению"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Направление"
        verbose_name_plural: str = "Направления"

    def __str__(self) -> str:
        return self.name


class SubjectClassTopic(Model):
    subject: ForeignKey = ForeignKey(
        to=Subject,
        on_delete=CASCADE,
        verbose_name="Предмет"
    )
    class_number: ForeignKey = ForeignKey(
        to=Class,
        on_delete=CASCADE,
        verbose_name="Класс"
    )
    topic: ForeignKey = ForeignKey(
        to=Topic,
        on_delete=CASCADE,
        verbose_name="Тема"
    )

    class Meta:
        verbose_name: str = "Тема класса"
        verbose_name_plural: str = "Темы классов"
        constraints: list[Any] = [
            UniqueConstraint(
                fields=['subject', 'class_number', 'topic'],
                name="unique_subject_class_number_topic"
            ),
        ]
