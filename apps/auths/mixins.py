from typing import Optional

from auths.models import CustomUser


class EmailObjectMixin:
    """Mixin for getting user via provided email."""

    def get_user_by_email(self, email: str) -> Optional[CustomUser]:
        """Get user|None object by the provided email."""
        obj: Optional[CustomUser] = None
        try:
            obj = CustomUser.objects.select_related(
                "student",
                "teacher",
                "teacher__subscription",
                "teacher__status_subscription",
            ).get(email=email)
            return obj
        except CustomUser.DoesNotExist:
            return None
