from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)


from auths.models import CustomUser
from abstracts.serializers import AbstractDateTimeSerializer


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
