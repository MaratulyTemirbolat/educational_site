from typing import Tuple

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)

from subjectss.models import (
    GeneralSubject,
    TrackWay,
    Class,
)
from abstracts.serializers import AbstractDateTimeSerializer


class GeneralSubjectBaseSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """GeneralSubjectBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the GeneralSubject model reference."""

        model: GeneralSubject = GeneralSubject
        fields: str | tuple[str] = "__all__"


class TrackWayBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """TrackWayBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        model: TrackWay = TrackWay
        fields: str | Tuple[str] = (
            "id",
            "name",
            "datetime_created",
            "datetime_deleted",
            "is_deleted",
        )


class TrackWayDetailSerializer(TrackWayBaseSerializer):
    """TrackWayDetailSerializer."""

    subjects: GeneralSubjectBaseSerializer = GeneralSubjectBaseSerializer(
        many=True
    )

    class Meta:
        model: TrackWay = TrackWay
        fields: str | tuple[str] = "__all__"


class ClassBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """ClassBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        model: Class = Class
        fields: str | tuple[str] = (
            "id",
            "number",
            "datetime_created",
            "is_deleted",
        )
