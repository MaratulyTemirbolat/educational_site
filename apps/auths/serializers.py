from typing import Union
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    Serializer,
    EmailField,
    CharField,
)

from auths.models import CustomUser
from abstracts.serializers import AbstractDateTimeSerializer
from subjectss.serializers import StudentForeignSerializer
from teaching.serializers import TeacherForeignModelSerializer
from subjectss.models import Student
from teaching.models import Teacher


class CustomUserSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """CustomUserSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "datetime_created",
            "is_deleted",
        )


class DetailCustomUserSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """DetailCustomUserSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    student: StudentForeignSerializer = StudentForeignSerializer()
    teacher: TeacherForeignModelSerializer = TeacherForeignModelSerializer()

    class Meta:
        """Customization of the table."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "datetime_created",
            "is_deleted",
            "is_staff",
            "is_active",
            "groups",
            "student",
            "teacher",
        )


class CreateCustomUserSerializer(ModelSerializer):
    """CreateCustomUserSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "email",
            "first_name",
            "last_name",
            "password",
        )


class ForeignCustomUserSerializer(ModelSerializer):
    """ForeignCustomUserSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "id",
            "email",
            "first_name",
            "last_name",
        )


class CustomUserListStudentSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """CustomUserListStudentSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    student: StudentForeignSerializer = StudentForeignSerializer()

    class Meta:
        model: CustomUser = CustomUser
        fields: Union[str, tuple[str]] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_deleted",
            "datetime_created",
            "student",
        )


class CustomUserListTeacherSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """CustomUserListTeacherSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    teacher: TeacherForeignModelSerializer = TeacherForeignModelSerializer()

    class Meta:
        model: CustomUser = CustomUser
        fields: Union[str, tuple[str]] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_deleted",
            "datetime_created",
            "teacher",
        )


class CustomUserLoginSerializer(Serializer):
    """CustomUserLoginSerializer."""

    email: EmailField = EmailField()
    password: CharField = CharField()

    class Meta:
        """Customization of the Serializer."""
        fields: tuple[str] = (
            "email",
            "password",
        )


class CustomUserForeignSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """CustomUserForeignSerializer."""

    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the serializer."""

        model: CustomUser = CustomUser
        fields: Union[tuple[str], str] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "datetime_created",
            "is_deleted",
        )


class StudentChatForeignSerializer(ModelSerializer):
    """StudentChatSerializer."""
    user: CustomUserForeignSerializer = CustomUserForeignSerializer()

    class Meta:
        model: Student = Student
        fields: Union[str, tuple[str]] = (
            "id",
            "user",
            "points",
        )


class TeacherChatForeignSerializer(ModelSerializer):
    """TeacherChatForeignSerializer."""

    user: CustomUserForeignSerializer = CustomUserForeignSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Teacher = Teacher
        fields: Union[tuple[str], str] = (
            "id",
            "user",
        )


utc = pytz.UTC


class TeacherListModelSerializer(TeacherForeignModelSerializer):
    """TeacherListModelSerializer."""

    user: CustomUserForeignSerializer = CustomUserForeignSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Teacher = Teacher
        fields: Union[tuple[str], str] = (
            "id",
            "user",
            "status_subscription",
            "datetime_created",
            "is_expired_subscrs",
            "tought_subjects",
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
