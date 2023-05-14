from typing import (
    Optional,
    Any,
    Union,
)

from django.contrib.admin import (
    ModelAdmin,
    register,
)
from django.utils.safestring import mark_safe
from django.core.handlers.wsgi import WSGIRequest

from abstracts.admin import AbstractAdminIsDeleted
from abstracts.filters import DeletedStateFilter
from subjectss.filters import PointsFilter
from subjectss.models import (
    Topic,
    Class,
    TrackWay,
    StudentSubjectState,
    GeneralSubject,
    ClassSubject,
    StudentRegisteredSubjects,
    Student,
)


@register(Topic)
class TopicAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "name",
        "get_short_content",
        "attached_subect_class",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "name",
    )
    list_filter: tuple[Any] = (
        DeletedStateFilter,
        "attached_subect_class",
    )
    search_fields: tuple[str] = (
        "id",
        "name",
        "content",
    )
    list_select_related: tuple[str] = (
        "attached_subect_class",
    )
    ordering: tuple[str] = ("-datetime_updated", "-datetime_created", "-id")
    save_on_top: bool = True
    list_per_page: int = 20
    save_as: bool = True
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Информация о теме",
            {
                "fields": (
                    "name",
                    "attached_subect_class",
                    "content",
                )
            }
        ),
        (
            "Файл контента/Ввидео ссылка",
            {
                "fields": (
                    "content_file",
                    "video_url",
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

    def get_short_content(self, obj: Optional[Topic] = None) -> str:
        """Get shortened content of the topic."""
        return f"{obj.content[:50]}..." if obj else "No content"
    get_short_content.short_description = "Контент"

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Topic] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + (
                "name",
                "video_url",
                "attached_subect_class",
            )
        return self.readonly_fields


@register(Class)
class ClassAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "number",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "number",
    )
    search_fields: tuple[str] = (
        "id",
        "number",
    )
    list_filter: tuple[Any, str] = (
        "number",
        DeletedStateFilter,
    )
    fields: tuple[str] = (
        "number",
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )
    ordering: tuple[str] = ("-datetime_updated", "-datetime_created", "-id",)
    list_per_page: int = 15
    save_as: bool = True

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Class] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("number",)
        return self.readonly_fields


@register(GeneralSubject)
class GeneralSubjectAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = ("id", "name", "get_is_deleted_obj",)
    list_display_links: tuple[str] = ("id", "name",)
    list_filter: tuple[Any] = (DeletedStateFilter,)
    search_fields: tuple[str] = ("id", "name",)
    ordering: tuple[str] = ("-datetime_updated", "-id",)
    fields: tuple[str] = (
        "name",
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )
    save_as: bool = True
    save_on_top: bool = True
    list_per_page: int = 15

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[GeneralSubject] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("name",)
        return self.readonly_fields


@register(StudentSubjectState)
class StudentSubjectStateAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = ("id", "name", "get_is_deleted_obj",)
    list_display_links: tuple[str] = ("id", "name",)
    list_filter: tuple[Any] = (DeletedStateFilter, "name",)
    search_fields: tuple[str] = ("id", "name",)
    ordering: tuple[str] = ("-datetime_updated", "-id",)
    fields: tuple[str] = (
        "name",
        "datetime_created",
        "datetime_updated",
        "datetime_deleted",
    )
    save_as: bool = True
    save_on_top: bool = True
    list_per_page: int = 15

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[StudentSubjectState] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("name",)
        return self.readonly_fields


@register(StudentRegisteredSubjects)
class StudentRegisteredSubjectsAdmin(ModelAdmin):
    list_select_related: tuple[str] = (
        "student",
        "class_subject",
        "current_state",
        "student__user",
    )
    list_display: tuple[str] = (
        "id",
        "student",
        "class_subject",
        "get_student_subj_state",
    )
    list_display_links: tuple[str] = (
        "id",
        "student",
        "class_subject",
    )
    list_filter: tuple[str] = ("current_state",)
    search_fields: tuple[str] = (
        "student__user__first_name",
        "student__user__last_name",
        "class_subject__name",
    )
    list_per_page: int = 20
    save_as: bool = True
    save_on_top: bool = True

    def get_student_subj_state(
        self,
        obj: Optional[StudentRegisteredSubjects] = None,
    ) -> str:
        """Get is deleted state of object."""
        colors: dict[str, str] = {
            "заблокирован": "black",
            "закрытый": "orange",
            "активный": "green",
            "заброшен": "gray",
            "завален": "red",
        }
        if obj.current_state:
            return mark_safe(
                f'<p style="color:\
                    {colors.get(obj.current_state.name.lower(), "purple")};\
                        font-weight: bold; font-size: 17px;">\
                            {obj.current_state}</p>'
            )
        return mark_safe(
            '<p style="font-weight: bold; font-size: 17px;">-</p>'
        )
    get_student_subj_state.short_description = "Текущее состояние"

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[StudentRegisteredSubjects] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("student", "class_subject",)
        return self.readonly_fields


@register(ClassSubject)
class ClassSubjectAdmin(AbstractAdminIsDeleted, ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "name",
        "general_subject",
        "attached_class",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "name",
    )
    list_select_related: tuple[str] = (
        "general_subject",
        "attached_class",
    )
    list_filter: tuple[Any] = (
        DeletedStateFilter,
        "general_subject",
        "attached_class",
    )
    search_fields: tuple[str] = (
        "name",
        "general_subject__name",
        "attached_class__number",
    )
    list_per_page: int = 20
    save_as: bool = True
    save_on_top: bool = True
    ordering: tuple[str] = ("-datetime_updated", "-id",)
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "general_subject",
                    "attached_class",
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
        obj: Optional[ClassSubject] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + (
                "general_subject",
                "attached_class",
            )
        return self.readonly_fields


@register(TrackWay)
class TrackWayAdmin(AbstractAdminIsDeleted, ModelAdmin):
    fieldsets: tuple[tuple[Union[str, dict[str, Any]]]] = (
        (
            "Основная информация о направлении (трэке)",
            {
                "fields": (
                    "name",
                    "subjects",
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
    list_display: tuple[str] = (
        "id",
        "name",
        "get_is_deleted_obj",
    )
    list_display_links: tuple[str] = (
        "id",
        "name",
    )
    list_filter: tuple[Any] = (DeletedStateFilter,)
    search_fields: tuple[str] = ("id", "name",)
    ordering: tuple[str] = ("-datetime_updated",)
    filter_horizontal: tuple[str] = ("subjects",)
    list_per_page: int = 15
    save_as: bool = True
    save_on_top: bool = True


@register(Student)
class StudentAdmin(ModelAdmin):
    list_select_related: tuple[str] = (
        "user",
    )
    list_display: tuple[str] = (
        "id",
        "user",
        "points",
    )
    list_display_links: tuple[str] = (
        "id",
        "user",
    )
    search_fields: tuple[str] = (
        "id",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    fields: tuple[str] = ("user", "points",)
    list_filter: tuple[Any] = (PointsFilter,)

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Student] = None
    ) -> tuple[str]:
        if obj:
            return self.readonly_fields + ("points", "user",)
        return self.readonly_fields
