from typing import (
    Optional,
    Any,
)

from django.utils.safestring import mark_safe

from abstracts.models import AbstractDateTime
from abstracts.filters import DeletedStateFilter


class AbstractAdminIsDeleted:

    readonly_fields: tuple[str] = (
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )
    list_filter: tuple[Any] = (DeletedStateFilter,)

    def get_is_deleted_obj(
        self,
        obj: Optional[AbstractDateTime] = None,
        obj_name: str = "Объект"
    ) -> str:
        """Get is deleted state of object."""
        if obj.datetime_deleted:
            return mark_safe(
                f'<p style="color:red; font-weight: bold; font-size: 16px;">\
                    {obj_name} удалён</p>'
            )
        return mark_safe(
            f'<p style="color: green; font-weight: bold; font-size: 16px;">\
                {obj_name} не удалён</p>'
        )
    get_is_deleted_obj.short_description = "Состояние объекта"
