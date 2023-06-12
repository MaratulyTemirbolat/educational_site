from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
)

from abstracts.serializers import AbstractDateTimeSerializer

from chats.models import PersonalChat
from auths.serializers import (
    StudentChatForeignSerializer,
    TeacherChatForeignSerializer,
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
        fields: tuple[str] | str = (
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
