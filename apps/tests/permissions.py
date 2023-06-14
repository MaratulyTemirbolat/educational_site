from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request as DRF_Request

from tests.models import Quiz


class IsQuizStudent(BasePermission):
    message: str = "Вы не можете запрашивать чужой тест."

    def has_object_permission(
        self,
        request: DRF_Request,
        view: Any,
        obj: Quiz
    ):
        """Check whether the student if a quiz owner."""
        return bool(obj.student == request.user.student)
