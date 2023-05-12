from typing import Any

from django.db.models import (
    TextField,
    ForeignKey,
    UniqueConstraint,
    CASCADE,
)

from abstracts.models import AbstractDateTime
from auths.models import CustomUser
from subjectss.models import Student
from teaching.models import Teacher


class PersonalChat(AbstractDateTime):
    student: Student = ForeignKey(
        to=Student,
        on_delete=CASCADE,
        related_name="personal_chats",
        verbose_name="Студент"
    )
    teacher: Teacher = ForeignKey(
        to=Teacher,
        on_delete=CASCADE,
        related_name="personal_chats",
        verbose_name="Преподаватель"
    )

    class Meta:
        verbose_name: str = "Личный чат"
        verbose_name_plural: str = "Личные чаты (переписки)"
        ordering: tuple[str] = ("-datetime_updated",)
        constraints: tuple[Any] = [
            UniqueConstraint(
                fields=['student', 'teacher'],
                name="unique_student_teacher_chat"
            ),
        ]

    def __str__(self) -> str:
        return f"Чат студента {self.student} с преподавателем {self.teacher}"


class Message(AbstractDateTime):
    content: TextField = TextField(
        verbose_name="Текст сообщения"
    )
    owner: CustomUser = ForeignKey(
        to=CustomUser,
        on_delete=CASCADE,
        related_name="messages",
        verbose_name="Владелец/Создатель"
    )
    to_chat: PersonalChat = ForeignKey(
        to=PersonalChat,
        on_delete=CASCADE,
        related_name="messages",
        verbose_name="В какой чат отправить сообщение"
    )

    class Meta:
        verbose_name: str = "Сообщение"
        verbose_name_plural: str = "Сообщения"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return f"Сообщение {self.content[:40]}"
