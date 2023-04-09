from typing import Optional

from django.db.models import (
    QuerySet,
    Model,
)

from abstracts.models import AbstractDateTimeQuerySet


class ModelInstanceMixin:
    """MIxin for getting instance."""

    def get_queryset_instance(
        self,
        class_name: Model,
        queryset: QuerySet,
        pk: int = 0,
    ) -> Optional[Model]:
        """Get class instance by PK with provided queryset."""
        if not isinstance(queryset, QuerySet):
            return None
        obj: Optional[Model] = None
        try:
            obj = queryset.get(pk=pk)
            return obj
        except class_name.DoesNotExist:
            return None

    def get_queryset_instance_by_id(
        self,
        class_name: Model,
        queryset: QuerySet,
        pk: int = 0,
        is_deleted: bool = False
    ) -> Optional[Model]:
        """Get class instance by PK with provided queryset."""
        if not isinstance(queryset, AbstractDateTimeQuerySet):
            return None
        obj: Optional[Model] = None
        try:
            if is_deleted:
                obj = queryset.get_deleted().get(pk=pk)
            else:
                obj = queryset.get_not_deleted().get(pk=pk)
            return obj
        except class_name.DoesNotExist:
            return None
