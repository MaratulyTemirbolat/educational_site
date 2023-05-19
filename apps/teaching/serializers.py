from typing import Tuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
)
from subscriptions.serializers import (
    SubscriptionForeignSerializer,
    StatusForeignSerializer,
)
from teaching.models import Teacher

utc = pytz.UTC


class TeacherForeignModelSerializer(ModelSerializer):
    """Serializer where Teacher is used as a foreign key with short data."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        read_only=True
    )
    is_expired_subscrs: SerializerMethodField = SerializerMethodField(
        method_name="get_is_expired_subscription"
    )
    subscription: SubscriptionForeignSerializer = \
        SubscriptionForeignSerializer()
    status_subscription: StatusForeignSerializer = StatusForeignSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Teacher = Teacher
        fields: Tuple[str] | str = (
            "id",
            "user",
            "subscription",
            "status_subscription",
            "datetime_created",
            "is_expired_subscrs",
        )

    def get_is_expired_subscription(self, obj: Teacher) -> bool:
        """Get if the subscription is expired or not."""
        if not obj.subscription or not obj.datetime_created:
            return None
        cur_datetime: datetime = datetime.now(tz=utc)
        expired_datetime: datetime = (obj.datetime_created + relativedelta(
            months=obj.subscription.duration
        ))
        # expired_datetime = expired_datetime.replace(tzinfo=utc)

        return True if cur_datetime > expired_datetime else False


class TeacherBaseModelSerializer(ModelSerializer):
    """TeacherBaseModelSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Teacher = Teacher
        fields: Tuple[str] | str = "__all__"
