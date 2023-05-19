from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from teaching.models import Teacher


class IsTeacherOrUser(BasePermission):
    """IsNonDeletedUser."""

    message: str = 'Ваш уровень доступа ниже учителя или вы удалены/заблокировы'

    def is_not_deleted_user(
        self,
        request: DRF_Request,
    ) -> bool:
        """Get is user deleted or not."""
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.datetime_deleted and
            request.user.is_active
        )

    def is_teacher(self, request: DRF_Request) -> bool:
        """Get is user deleted or not."""
        return Teacher.objects.filter(user_id=request.user.id).exists() \
            if request.user.is_authenticated else False

    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        """Handle request permissions."""
        return bool(
            self.is_not_deleted_user(request=request) and
            self.is_teacher(request=request) or
            (
                request.user.is_superuser and
                not request.user.datetime_deleted and
                request.user.is_active
            )
        )
