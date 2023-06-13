from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from chats.models import PersonalChat


class IsChatMember(BasePermission):
    """IsCustomAdminUser."""

    message: str = "Вы не являетесь участником чата."

    def has_object_permission(
        self,
        request: DRF_Request,
        view: Any,
        obj: PersonalChat
    ) -> bool:
        """Return true if user is in chat."""
        return bool(
            obj.student.user == request.user or
            obj.teacher.user == request.user or
            request.user.is_superuser
        )
