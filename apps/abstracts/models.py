from typing import Any
from datetime import datetime

from django.db.models import (
    Model,
    DateTimeField,
    QuerySet,
)


class AbstractDateTimeQuerySet(QuerySet):
    """AbstractDateTimeQuerySet."""

    def get_deleted(self) -> QuerySet[Model]:
        """Get deleted users."""
        return self.filter(
            datetime_deleted__isnull=False
        )

    def get_not_deleted(self) -> QuerySet[Model]:
        """Get not deleted users."""
        return self.filter(
            datetime_deleted__isnull=True
        )


class AbstractDateTime(Model):
    """AbstractDateTime model class."""

    datetime_created: DateTimeField = DateTimeField(
        verbose_name="время и дата создания",
        auto_now_add=True
    )
    datetime_updated: DateTimeField = DateTimeField(
        verbose_name="время и дата обновления",
        auto_now=True
    )
    datetime_deleted: DateTimeField = DateTimeField(
        verbose_name="время и дата удаления",
        null=True,
        blank=True
    )
    objects = AbstractDateTimeQuerySet.as_manager()

    class Meta:
        """Customization of the table."""

        abstract = True

    def save(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Override the save method."""
        super().save(*args, **kwargs)

    def delete(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Override default delete moethod."""
        datetime_now: datetime = datetime.now()
        self.datetime_deleted = datetime_now
        self.save(
            update_fields=['datetime_deleted']
        )
