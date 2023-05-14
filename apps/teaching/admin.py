from typing import (
    Union,
    Optional,
    Any,
)

from django.contrib.admin import (
    register,
    ModelAdmin,
)
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe

from teaching.models import Teacher


@register(Teacher)
class TeacherAdmin(ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "user",
        "subscription",
        "get_subscr_status",
        "datetime_created",
    )
    list_select_related: tuple[str] = (
        "user",
        "subscription",
        "status_subscription",
    )
    list_display_links: tuple[str] = (
        "id",
        "user",
    )
    search_fields: tuple[str] = (
        "id",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    list_filter: tuple[str] = (
        "subscription",
        "status_subscription",
    )
    readonly_fields: tuple[str] = (
        "datetime_created",
        "status_subscription",
    )
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация",
            {
                "fields": (
                    "user",
                    "tought_subjects",
                )
            }
        ),
        (
            "Информация о подписке",
            {
                "fields": (
                    "subscription",
                    "status_subscription",
                    "datetime_created",
                )
            }
        ),
    )
    date_hierarchy: str = "datetime_created"
    filter_horizontal: tuple[str] = ("tought_subjects",)
    list_per_page: int = 10
    save_as: bool = True
    save_on_top: bool = True

    def get_subscr_status(self, obj: Optional[Teacher] = None) -> str:
        """Get shortened content of the topic."""
        colors: dict[str, str] = {
            "активен": "green",
            "не активен": "red",
        }
        if obj.status_subscription:
            return mark_safe(
                f'<p style="color:\
                    {colors.get(obj.status_subscription.name.lower())};\
                        font-weight: bold; font-size: 16px;">\
                            {obj.status_subscription}</p>'
            )
        return mark_safe(
            '<p style="font-weight: bold; font-size: 16px;">Отсутствует</p>'
        )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Teacher] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + (
                "user",
                "subscription",
            )
        return self.readonly_fields
