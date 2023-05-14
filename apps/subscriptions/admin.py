from typing import (
    Optional,
    Any,
    Union,
)

from django.contrib.admin import register, ModelAdmin
from django.core.handlers.wsgi import WSGIRequest

from subscriptions.models import Subscription, Status
from abstracts.admin import AbstractAdminIsDeleted
from abstracts.filters import DeletedStateFilter


@register(Subscription)
class SubscriptionAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "name",
        "description",
        "duration",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = ("id", "name",)
    search_fields: tuple[str] = ("id", "name", "description",)
    list_filter: tuple[Any] = (
        "duration",
        DeletedStateFilter,
    )
    list_per_page: int = 15
    save_as: bool = True
    save_on_top: bool = True
    empty_value_display: str = "Не установлено"
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Главная информация",
            {
                "fields": (
                    "name",
                    "description",
                    "duration",
                )
            }
        ),
        (
            "Данные состояния сообщения",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Subscription] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + (
                "name",
                "duration",
            )
        return self.readonly_fields


@register(Status)
class StatusAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = ("id", "name", "get_is_deleted_obj",)
    list_display_links: tuple[str] = ("id", "name",)
    search_fields: tuple[str] = ("name", "id",)
    list_per_page: int = 15
    empty_value_display: str = "Не установлено"
    save_as: bool = True
    save_on_top: bool = True
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Главная информация",
            {
                "fields": (
                    "name",
                )
            }
        ),
        (
            "Данные состояния сообщения",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Subscription] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("name",)
        return self.readonly_fields
