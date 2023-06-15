from typing import (
    Optional,
    Tuple,
    Union,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

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

    def get_obj_or_response(
        self,
        request: DRF_Request,
        pk: Union[int, str],
        class_name: Model,
        queryset: QuerySet[Model],
        is_deleted: bool = False,
    ) -> Tuple[Union[Model, DRF_Response], bool]:
        """Return object and boolean as True. Otherwise Response and False."""
        if is_deleted and not request.user.is_superuser:
            return (DRF_Response(
                data={
                    "message": "Вы не админ, чтобы получать удаленных юзеров"
                },
                status=HTTP_403_FORBIDDEN
            ), False)
        obj: Optional[Model] = None
        obj = self.get_queryset_instance(
            class_name=class_name,
            queryset=queryset,
            pk=pk
        )
        if not obj:
            return (DRF_Response(
                data={
                    "response": f"Объект с ID: {pk} не найден или удалён"
                },
                status=HTTP_404_NOT_FOUND
            ), False)
        return (obj, True)
