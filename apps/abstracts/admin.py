from typing import Optional

from django.utils.safestring import mark_safe

from apps.abstracts.models import AbstractDateTime


class AbstractAdminIsDeleted:

    readonly_fields: tuple[str] = (
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )

    def get_is_deleted_obj(
        self,
        obj: Optional[AbstractDateTime] = None,
        obj_name: str = "Объект"
    ) -> str:
        """Get is deleted state of object."""
        if obj.datetime_deleted:
            return mark_safe(
                f'<p style="color:red; font-weight: bold; font-size: 17px;">\
                    {obj_name} удалён</p>'
            )
        return mark_safe(
            f'<p style="color: green; font-weight: bold; font-size: 17px;">\
                {obj_name} не удалён</p>'
        )
