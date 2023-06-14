from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from subjectss.models import Student


class IsStudent(BasePermission):
    def has_permission(self, request: DRF_Request, view: Any) -> bool:
        """Handle request permissions."""
        return bool(
            request.user and
            request.user.is_authenticated and
            not request.user.datetime_deleted and
            Student.objects.filter(user=request.user).exists()
        )
