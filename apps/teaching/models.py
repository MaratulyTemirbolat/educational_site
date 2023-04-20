from typing import Any, Optional
from datetime import datetime

from django.db.models import (
    OneToOneField,
    Model,
    ForeignKey,
    UniqueConstraint,
    ManyToManyField,
    DateTimeField,
    CASCADE,
)

from auths.models import CustomUser
from subscriptions.models import Subscription, Status
from subjectss.models import Subject, Class
from teaching.validators import validate_teacher_update


class Teacher(Model):
    user: CustomUser = OneToOneField(
        to=CustomUser,
        on_delete=CASCADE,
        verbose_name="Пользователь"
    )
    tought_subjects: ManyToManyField = ManyToManyField(
        to=Subject,
        through="TeacherSubjectClass",
        through_fields=("teacher", "subject"),
        related_name="subjects",
        verbose_name="Предметы"
    )
    subscription: ForeignKey = ForeignKey(
        to=Subscription,
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="used_by",
        verbose_name="Подписка"
    )
    status_subscription: ForeignKey = ForeignKey(
        to=Status,
        on_delete=CASCADE,
        blank=True,
        null=True,
        verbose_name="Статус подписки"
    )
    datetime_created: DateTimeField = DateTimeField(
        blank=True,
        null=True,
        verbose_name="Время и дата получения подписки"
    )

    __old_subscription: Optional[Subscription] = None

    class Meta:
        verbose_name: str = "Преподаватель"
        verbose_name_plural: str = "Преподаватели"
        ordering: tuple[str] = ("-id",)

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.__old_subscription = self.subscription

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def clean(self) -> None:
        print("clean")
        return super().clean()

    def full_clean(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        print("full_clean")
        validate_teacher_update(self)
        return super().full_clean(*args, **kwargs)

    def save(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        if self._state.adding and self.subscription:
            self.datetime_created = datetime.now()
            self.status_subscription_id = 1
        if self.subscription != self.__old_subscription:
            print("Subscription Changed")
            # Do some code
        print("save")
        self.__old_subscription = self.subscription
        return super().save(*args, **kwargs)


class TeacherSubjectClass(Model):
    teacher: Teacher = ForeignKey(
        to=Teacher,
        on_delete=CASCADE,
        verbose_name="Преподаватель"
    )
    subject: Subject = ForeignKey(
        to=Subject,
        on_delete=CASCADE,
        verbose_name="Ведущий предмет"
    )
    clas: Class = ForeignKey(
        to=Class,
        on_delete=CASCADE,
        verbose_name="Возможные классы"
    )

    class Meta:
        verbose_name: str = "Предмет преподавателя с классом"
        verbose_name_plural: str = "Предметы преподавателей с классами"
        ordering: tuple[str] = ("-id",)
        constraints: list[Any] = [
            UniqueConstraint(
                fields=['teacher', 'subject', 'clas'],
                name="unique_teacher_subject_clas"
            ),
        ]
