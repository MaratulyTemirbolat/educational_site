from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    QuerySet,
)

from abstracts.models import AbstractDateTime


class CustomUserManager(BaseUserManager):
    """CustomUserManger."""

    def __obtain_user_instance(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Get user instance."""
        if not email:
            raise ValidationError(
                message="Email field is required",
                code="email_empty"
            )
        if first_name.replace(" ", "") == "":
            raise ValidationError(
                message="First name is required.",
                code="firt_name_empty"
            )

        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )
        return new_user

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Create Custom user."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]  # kwargs -> key word arguments
    ) -> 'CustomUser':
        """Create super user."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def get_deleted(self) -> QuerySet:
        """Get deleted users."""
        return self.filter(
            datetime_deleted__isnull=False
        )

    def get_not_deleted(self) -> QuerySet:
        """Get not deleted users."""
        return self.filter(
            datetime_deleted__isnull=True
        )


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractDateTime
):
    """CustomUser model database."""

    email: EmailField = EmailField(
        unique=True,
        db_index=True,
        verbose_name="Почта/Логин"
    )
    first_name: CharField = CharField(
        max_length=200,
        verbose_name="Имя"
    )
    last_name: CharField = CharField(
        max_length=200,
        verbose_name="Фамилия"
    )
    is_active: BooleanField = BooleanField(
        default=True,
        verbose_name="Активность",
        help_text="True - ваш акк активный, False - удален"
    )
    is_staff: BooleanField = BooleanField(
        default=False,
        verbose_name="Статус менеджера"
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = [
        "first_name", "last_name",
    ]

    class Meta:
        """Customization of the Model (table)."""

        ordering: tuple[str] = (
            "-datetime_updated",
        )
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
