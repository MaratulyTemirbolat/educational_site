from typing import (
    Any,
    Union,
)

from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
    HiddenField,
    CurrentUserDefault,
)

from abstracts.serializers import AbstractDateTimeSerializer

from chats.models import (
    PersonalChat,
    Message,
)
from auths.serializers import (
    StudentChatForeignSerializer,
    TeacherChatForeignSerializer,
    CustomUserForeignSerializer,
)
from abstracts.paginators import AbstractPageNumberPaginator


class CurrentChatSerializer:

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['to_chat']

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class MessageBaseModelSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """MessageBaseModelSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    owner: CustomUserForeignSerializer = CustomUserForeignSerializer()

    class Meta:
        model: Message = Message
        fields: Union[str, tuple[str]] = (
            "id",
            "content",
            "owner",
            "is_deleted",
            "datetime_created",
        )


class MessageCreateModelSerializer(ModelSerializer):
    """MessageCreateModelSerializer."""

    owner: HiddenField = HiddenField(
        default=CurrentUserDefault()
    )
    to_chat: HiddenField = HiddenField(
        default=CurrentChatSerializer()
    )

    class Meta:
        """Customization of the Serializer."""

        model: Message = Message
        fields: Union[tuple[str], str] = (
            "id",
            "content",
            "owner",
            "to_chat",
        )


class PersonalChatBaseModelSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """PersonalChatBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        model: PersonalChat = PersonalChat
        fields: Union[tuple[str], str] = (
            "id",
            "is_deleted",
            "datetime_created",
            "student",
            "teacher",
        )


class PersonalChatListSerializer(PersonalChatBaseModelSerializer):
    """PersonalChatListSerializer."""

    student: StudentChatForeignSerializer = StudentChatForeignSerializer()
    teacher: TeacherChatForeignSerializer = TeacherChatForeignSerializer()


class PersonalChatDetailSerializer(PersonalChatListSerializer):
    """PersonalChatDetailSerializer."""

    messages: SerializerMethodField = SerializerMethodField(
        method_name="get_paginated_messages"
    )
    # Good too, but without pagination
    # messages: MessageBaseModelSerializer = MessageBaseModelSerializer(
    #     many=True
    # )

    class Meta:
        """Customization of the Serializer."""

        model: PersonalChat = PersonalChat
        fields: Union[tuple[str], str] = (
            "id",
            "is_deleted",
            "datetime_created",
            "student",
            "teacher",
            "messages",
        )

    def get_paginated_messages(self, obj: PersonalChat) -> dict[str, Any]:
        """Get paginated messages."""
        paginator: AbstractPageNumberPaginator = AbstractPageNumberPaginator()
        paginator.page_size = self.context['request'].query_params.get(
            'size'
        ) or 30
        objects: list[Any] = paginator.paginate_queryset(
            queryset=obj.messages.select_related(
                "owner"
            ).order_by("-datetime_created"),
            request=self.context['request']
        )
        serializer: MessageBaseModelSerializer = MessageBaseModelSerializer(
            instance=objects,
            many=True
        )
        return paginator.get_dict_response(data=serializer.data)
