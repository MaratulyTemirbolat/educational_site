from typing import Any, Optional
from datetime import datetime

from django.db.models import (
    OneToOneField,
    Model,
    ForeignKey,
    ManyToManyField,
    DateTimeField,
    CASCADE,
)

from auths.models import CustomUser
from subscriptions.models import Subscription, Status
from subjectss.models import ClassSubject
from teaching.validators import validate_teacher_update


class Teacher(Model):
    user: CustomUser = OneToOneField(
        to=CustomUser,
        on_delete=CASCADE,
        related_name="teacher",
        verbose_name="Пользователь"
    )
    tought_subjects: ManyToManyField = ManyToManyField(
        to=ClassSubject,
        blank=True,
        related_name="teachers",
        verbose_name="Преподаваемые предметы"
    )
    subscription: Subscription = ForeignKey(
        to=Subscription,
        on_delete=CASCADE,
        blank=True,
        null=True,
        related_name="used_by",
        verbose_name="Подписка"
    )
    status_subscription: Status = ForeignKey(
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
        return f"Преподаватель {self.user}"

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
