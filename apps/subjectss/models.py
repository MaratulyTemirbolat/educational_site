from typing import Any

from django.db.models import (
    CharField,
    IntegerField,
    ManyToManyField,
    Model,
    ForeignKey,
    FileField,
    TextField,
    URLField,
    OneToOneField,
    UniqueConstraint,
    CASCADE,
)

from auths.models import CustomUser
from auths.validators import validate_negative_int
from apps.abstracts.models import AbstractDateTime
from apps.subjectss.validators import validate_negative_class_number


class StudentSubjectState(AbstractDateTime):
    STATE_NAME_LIM = 200

    name: CharField = CharField(
        max_length=STATE_NAME_LIM,
        unique=True,
        db_index=True,
        verbose_name="Наименование состояния"
    )

    class Meta:
        verbose_name: str = "Состояние взятого студентом предмета"
        verbose_name_plural: str = "Состояния взятого студентом предметов"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return self.name


class GeneralSubject(AbstractDateTime):
    SUBJECT_NAME_LIMIT = 200
    name: CharField = CharField(
        max_length=SUBJECT_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )

    class Meta:
        verbose_name: str = "Предмет"
        verbose_name_plural: str = "Предметы"
        ordering: tuple[str] = ("-datetime_updated",)

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


class ClassSubject(AbstractDateTime):
    SUBJECT_NAME_LIMIT = 200

    name: CharField = CharField(
        max_length=SUBJECT_NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )
    general_subject: GeneralSubject = ForeignKey(
        to=GeneralSubject,
        on_delete=CASCADE,
        related_name="class_subjects",
        verbose_name="Общий предмет",
        help_text="Обобщенный предмет к которому относится предмет класса"
    )
    attached_class: Class = ForeignKey(
        to=Class,
        on_delete=CASCADE,
        related_name="subjects",
        verbose_name="Относится к классу",
        help_text="Класс к которому относится данный предмет"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Предмет по классу"
        verbose_name_plural: str = "Предметы по классам"

    def __str__(self) -> str:
        return self.name


class Topic(AbstractDateTime):
    TOPIC_NAME_LIMIT = 240
    VIDEO_LINK_URL = 250

    name: CharField = CharField(
        max_length=TOPIC_NAME_LIMIT,
        verbose_name="Название"
    )
    content: TextField = TextField(
        verbose_name="Текстовый материал"
    )
    content_file: FileField = FileField(
        upload_to="documents/topic_files/%Y/%m/%d",
        null=True,
        blank=True,
        verbose_name="Файл с текстовым материалом"
    )
    video_url: URLField = URLField(
        max_length=VIDEO_LINK_URL,
        verbose_name="Ссылка на видео файл",
    )
    attached_subect_class: ForeignKey = ForeignKey(
        to=ClassSubject,
        on_delete=CASCADE,
        related_name="topics",
        verbose_name="Предмет класса",
        help_text="К какому предмету относится данная тема"
    )

    class Meta:
        ordering: tuple[str] = ("-datetime_updated",)
        verbose_name: str = "Тема предмета"
        verbose_name_plural: str = "Темы предметов"

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
        to=GeneralSubject,
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


class Student(Model):
    user: CustomUser = OneToOneField(
        to=CustomUser,
        on_delete=CASCADE,
        verbose_name="Пользователь"
    )
    points: IntegerField = IntegerField(
        default=0,
        validators=[validate_negative_int],
        verbose_name="Баллы"
    )
    registered_subjects: ManyToManyField = ManyToManyField(
        to=ClassSubject,
        blank=True,
        through="StudentRegisteredSubjects",
        through_fields=("student", "class_subject",),
        verbose_name="Зарегестрированные предметы"
    )

    class Meta:
        verbose_name: str = "Обучающийся"
        verbose_name_plural: str = "Обучающиеся"
        ordering: tuple[str] = ("-id",)

    def __str__(self) -> str:
        return f"Студент {self.user}"


class StudentRegisteredSubjects(Model):
    student: Student = ForeignKey(
        to=Student,
        on_delete=CASCADE,
        related_name="student_class_subjects",
        verbose_name="Студент, взявший предмет"
    )
    class_subject: ClassSubject = ForeignKey(
        to=ClassSubject,
        on_delete=CASCADE,
        related_name="student_class_subjects",
        verbose_name="Предмет класса"
    )
    current_state: StudentSubjectState = ForeignKey(
        to=StudentSubjectState,
        on_delete=CASCADE,
        related_name="student_class_subjects",
        verbose_name="Текущее состояние"
    )

    class Meta:
        verbose_name_plural: str = "Зарегестрированные предметы студента"
        verbose_name: str = "Зарегестрированный предмет студента"
        constraints: tuple[Any] = [
            UniqueConstraint(
                fields=['student', 'class_subject'],
                name="unique_student_class_subject"
            ),
        ]
