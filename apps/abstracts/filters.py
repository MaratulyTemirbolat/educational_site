from typing import (
    List,
    Tuple,
    Optional,
)

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin import ModelAdmin

from abstracts.models import AbstractDateTime


class DeletedStateFilter(SimpleListFilter):
    """DeletedStateFilter."""

    title: str = "Состояние"
    parameter_name: str = "pages"

    def lookups(
        self,
        request: WSGIRequest,
        model_admin: ModelAdmin
    ) -> List[Tuple[str, str]]:
        """Return tuple of value and verbose value."""
        return [
            ("deleted", "Удаленные объекты"),
            ("not_deleted", "Неудалённые объекты"),
        ]

    def queryset(
        self,
        request: WSGIRequest,
        queryset: QuerySet[AbstractDateTime]
    ) -> Optional[QuerySet[AbstractDateTime]]:
        """Return queryset by value."""
        if self.value() == "deleted":
            return queryset.filter(datetime_deleted__isnull=False)
        if self.value() == "not_deleted":
            return queryset.filter(datetime_deleted__isnull=True)
