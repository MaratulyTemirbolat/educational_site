from typing import Tuple

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)

from subscriptions.models import (
    Subscription,
    Status,
)
from abstracts.serializers import AbstractDateTimeSerializer


class SubscriptionBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """SubscriptionBaseSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted

    class Meta:
        """Customization of the Serializer."""

        model: Subscription = Subscription
        fields: Tuple[str] | str = "__all__"


class SubscriptionForeignSerializer(SubscriptionBaseSerializer):
    """SubscriptionForeignSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Subscription = Subscription
        fields: Tuple[str] | str = (
            "id",
            "name",
            "description",
            "duration",
            "datetime_created",
            "is_deleted",
        )


class StatusBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """StatusBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the Status Serializer."""

        model: Status = Status
        fields: Tuple[str] | str = "__all__"


class StatusForeignSerializer(StatusBaseSerializer):
    """StatusForeignSerializer."""

    class Meta:
        model: Status = Status
        fields: Tuple[str] | str = (
            "id",
            "name",
            "is_deleted",
            "datetime_created",
        )
