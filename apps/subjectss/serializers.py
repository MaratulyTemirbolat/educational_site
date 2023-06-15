from typing import (
    Dict,
    Tuple,
    Any,
    Union,
)

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)


from subjectss.models import (
    GeneralSubject,
    TrackWay,
    Class,
    ClassSubject,
    Topic,
    Student,
)
from abstracts.serializers import AbstractDateTimeSerializer
from abstracts.paginators import AbstractPageNumberPaginator


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
        fields: Union[str, tuple[str]] = (
            "id",
            "name",
            "datetime_created",
            "is_deleted",
        )


class ClassSubjectShortSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """ClassSubjectShortSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: ClassSubject = ClassSubject
        fields: Union[Tuple[str], str] = (
            "id",
            "name",
            "is_deleted",
            "datetime_created",
        )


class TopicBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """TopicBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    content: SerializerMethodField = SerializerMethodField(
        method_name="get_short_content"
    )

    class Meta:
        model: Topic = Topic
        fields: Union[str, tuple[str]] = (
            "id",
            "name",
            "content",
            "datetime_created",
            "is_deleted",
        )

    def get_short_content(self, obj: Topic) -> str:
        """Get shoted content."""
        return f"{obj.content[:50]}..." if obj else ""


class TopicListSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """TopicListSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    attached_subect_class: ClassSubjectShortSerializer = \
        ClassSubjectShortSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Topic = Topic
        exclude: Tuple[str] = (
            "content",
            "content_file",
            "video_url",
        )


class TopicDetailSerializer(TopicListSerializer):
    """TopicDetailSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Topic = Topic
        fields: Union[Tuple[str], str] = "__all__"


class TrackWayBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """TrackWayBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        model: TrackWay = TrackWay
        fields: Union[str, Tuple[str]] = (
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
        fields: Union[str, tuple[str]] = "__all__"


class ClassBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """ClassBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        model: Class = Class
        fields: Union[str, tuple[str]] = (
            "id",
            "number",
            "datetime_created",
            "is_deleted",
        )


class ClassSubjectBaseSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """ClassSubjectBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    attached_class: ClassBaseSerializer = ClassBaseSerializer()
    general_subject: GeneralSubjectBaseSerializer = \
        GeneralSubjectBaseSerializer()

    class Meta:
        model: ClassSubject = ClassSubject
        fields: Union[str, tuple[str]] = (
            "id",
            "name",
            "general_subject",
            "attached_class",
            "datetime_created",
            "is_deleted",
        )


class ClassSubjectDetailSerializer(ClassSubjectBaseSerializer):
    """ClassSubjectDetailSerializer."""

    topics: SerializerMethodField = SerializerMethodField(
        method_name="get_paginated_topics"
    )

    class Meta:
        model: ClassSubject = ClassSubject
        fields: Union[str, tuple[str]] = (
            "id",
            "name",
            "general_subject",
            "attached_class",
            "datetime_created",
            "is_deleted",
            "topics",
        )

    def get_paginated_topics(self, obj: ClassSubject) -> Dict[str, Any]:

        paginator: AbstractPageNumberPaginator = AbstractPageNumberPaginator()
        paginator.page_size = self.context['request'].query_params.get(
            'size'
        ) or 15
        objects: list = paginator.paginate_queryset(
            queryset=obj.topics.get_not_deleted().order_by("datetime_created"),
            request=self.context['request']
        )
        serializer: TopicBaseSerializer = TopicBaseSerializer(
            instance=objects,
            many=True
        )
        return paginator.get_dict_response(data=serializer.data)


class StudentForeignSerializer(ModelSerializer):
    """StudentForeignSerializer."""

    registered_subjects: ClassSubjectShortSerializer = \
        ClassSubjectShortSerializer(
            many=True,
            read_only=True
        )

    class Meta:
        model: Student = Student
        fields: Union[str, tuple[str]] = (
            "id",
            "points",
            "registered_subjects",
        )
