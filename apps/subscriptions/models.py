from django.db.models import (
    CharField,
    TextField,
    IntegerField,
)

from abstracts.models import AbstractDateTime


class Subscription(AbstractDateTime):
    NAME_LIMIT = 100
    name: CharField = CharField(
        max_length=NAME_LIMIT,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )
    description: TextField = TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    duration: IntegerField = IntegerField(
        default=3,
        verbose_name="Продолжительность в месяцах"
    )

    class Meta:
        verbose_name: str = "Подписка"
        verbose_name_plural: str = "Подписки"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Subscription):
            return self.pk == __value.pk
        return False


class Status(AbstractDateTime):
    name: CharField = CharField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name="Наименование"
    )

    class Meta:
        verbose_name: str = "Статус подписки"
        verbose_name_plural: str = "Статусы подписок"
        ordering: tuple[str] = ("-datetime_updated",)

    def __str__(self) -> str:
        return self.name
