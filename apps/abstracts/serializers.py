from typing import (
    Tuple,
    Dict,
    Any,
)

from rest_framework.serializers import (
    SerializerMethodField,
    DateTimeField,
)

from abstracts.models import AbstractDateTime


class AbstractDateTimeSerializer:
    """AbstractDateTimeSerializer."""

    is_deleted: SerializerMethodField = SerializerMethodField(
        method_name="get_is_deleted"
    )
    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        read_only=True
    )

    def get_is_deleted(
        self,
        obj: AbstractDateTime,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> bool:
        """Get is_deleted field."""
        if obj.datetime_deleted:
            return True
        return False
