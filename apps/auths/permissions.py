from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request


class IsNonDeletedUser(BasePermission):
    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        """Handle request permissions."""
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.datetime_deleted
        )


class IsCustomAdminUser(BasePermission):
    """IsCustomAdminUser."""

    message: str = "Вы не админ, чтобы запрашивать удалённых пользователей."

    def is_user_active(self, request: DRF_Request) -> bool:
        """Get is user active or not."""
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active
        )

    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))
        is_admin: bool = request.user.is_superuser
        if is_deleted and not is_admin:
            return False
        return True
