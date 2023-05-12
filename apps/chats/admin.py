from typing import (
    Optional,
    Union,
    Any,
)

from django.contrib.admin import (
    register,
    ModelAdmin,
)
from django.core.handlers.wsgi import WSGIRequest

from abstracts.admin import AbstractAdminIsDeleted
from abstracts.filters import DeletedStateFilter
from chats.models import (
    Message,
    PersonalChat,
)


@register(Message)
class MessageAdmin(AbstractAdminIsDeleted, ModelAdmin):
    date_hierarchy: str = "datetime_created"
    empty_value_display: str = "Не установлено"
    list_display: tuple[str] = (
        "id",
        "get_content",
        "owner",
        "to_chat",
        "get_is_deleted_obj",
    )
    list_filter: tuple[Any] = (
        DeletedStateFilter,
    )
    search_fields: tuple[str] = (
        "content",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )
    list_display_links: tuple[str] = ("id", "get_content",)
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Контент сообщения",
            {
                "fields": (
                    "content",
                )
            }
        ),
        (
            "Владелец и куда отправлено сообщение",
            {
                "fields": (
                    ("owner", "to_chat",),
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
    save_on_top: bool = True
    list_per_page: int = 15

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Message] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("owner", "to_chat",)
        return self.readonly_fields

    def get_content(self, obj: Optional[Message] = None) -> str:
        return f"{obj.content[:50]}..."


@register(PersonalChat)
class PersonalChatAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "student",
        "teacher",
        "get_is_deleted_obj"
    )
    list_display_links: tuple[str] = (
        "id",
        "student",
        "teacher",
    )
    search_fields: tuple[str] = (
        "student__user__email",
        "student__user__first_name",
        "student__user__last_name",
    )
    list_per_page: int = 20

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[PersonalChat] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("student", "teacher",)
        return self.readonly_fields
