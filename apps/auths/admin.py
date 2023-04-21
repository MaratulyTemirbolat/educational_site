from typing import (
    Sequence,
    Union,
    Any,
    Optional,
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auths.models import (
    CustomUser,
    Student,
)
from abstracts.filters import DeletedStateFilter
from abstracts.admin import AbstractAdminIsDeleted


@admin.register(CustomUser)
class CustomUserAdmin(AbstractAdminIsDeleted, UserAdmin):
    """CustomUser setting on Django admin site."""

    ordering: tuple[str] = ("email",)
    list_display: tuple[str] = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "get_is_deleted",
    )
    list_display_links: Sequence[str] = (
        "id",
        "email",
    )
    readonly_fields: tuple[str] = (
        "datetime_deleted",
        "datetime_created",
        "datetime_updated",
    )
    search_fields: Sequence[str] = (
        "email",
    )
    list_filter: tuple[str, Any] = (
        "is_active",
        "is_staff",
        "is_superuser",
        DeletedStateFilter,
    )
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Личная информация",
            {
                "fields": (
                    "email",
                    ("first_name", "last_name",),
                )
            }
        ),
        (
            "Разрешения (Доступы)",
            {
                "fields": (
                    ("is_superuser", "is_staff",),
                    "is_active",
                    "user_permissions",
                )
            }
        ),
        (
            "Данные времени",
            {
                "fields": (
                    "datetime_created",
                    "datetime_updated",
                    "datetime_deleted",
                )
            }
        )
    )
    add_fieldsets: tuple[tuple] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    save_on_top: bool = True
    list_per_page: int = 10

    def get_is_deleted(self, obj: Optional[CustomUser] = None) -> str:
        """Get is deleted state of object."""
        return self.get_is_deleted_obj(obj=obj, obj_name="Пользователь")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
