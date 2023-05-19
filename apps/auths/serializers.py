from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)


from auths.models import CustomUser
from abstracts.serializers import AbstractDateTimeSerializer
from subjectss.serializers import StudentForeignSerializer
from teaching.serializers import TeacherForeignModelSerializer


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
        fields: str | tuple[str] = (
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
        fields: str | tuple[str] = (
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
