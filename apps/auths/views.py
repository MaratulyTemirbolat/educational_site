from typing import (
    Dict,
    Optional,
    Tuple,
    Any,
    List,
)
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response as DRF_Response
from rest_framework.request import Request as DRF_Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
)

from django.db.models import QuerySet

from abstracts.mixins import ModelInstanceMixin
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator
from auths.models import (
    CustomUser,
    CustomUserManager,
)
from auths.serializers import (
    CustomUserSerializer,
    DetailCustomUserSerializer,
    CreateCustomUserSerializer,
)


class CustomUserViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """CustomUserViewSet."""

    queryset: CustomUserManager = CustomUser.objects
    permission_classes: tuple[Any] = (IsAuthenticated,)
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator

    def get_queryset(self) -> QuerySet[CustomUser]:
        """Get not deleted users."""
        return self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request."""
        is_deleted: bool = request.GET.get("is_deleted", False)
        if is_deleted and not request.user.is_superuser:
            message: str = "Вам нельзя запрашивать удалённых пользователей"
            return DRF_Response(
                data={
                    "response": message
                },
                status=status.HTTP_403_FORBIDDEN
            )
        sear_queryset: QuerySet[CustomUser] = self.queryset.get_deleted() \
            if is_deleted else self.get_queryset()
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=sear_queryset,
            serializer_class=CustomUserSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: str,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Hadnle GET-request with provided id."""
        is_deleted: bool = request.data.get("is_deleted", False)
        if not is_deleted:
            is_deleted = kwargs.get("is_deleted", False)

        custom_user: Optional[CustomUser] = None
        queryset: QuerySet[CustomUser]

        if not is_deleted:
            queryset = self.get_queryset()
        else:
            queryset = self.queryset.get_deleted()
        try:
            custom_user = queryset.get(pk=pk)
        except CustomUser.DoesNotExist:
            return DRF_Response(
                data={
                    "response": "Такого пользователя не существует или удален"
                }
            )
        serializer: DetailCustomUserSerializer = DetailCustomUserSerializer(
            instance=custom_user
        )
        return DRF_Response(
            data={
                "data": serializer.data
            }
        )

    @action(
        methods=["POST"],
        url_path="register_user",
        detail=False,
        permission_classes=(AllowAny,)
    )
    def create_user(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request for user creation."""
        is_superuser: bool = request.data.get("is_superuser", False)
        is_staff: bool = False

        if is_superuser and not request.user.is_superuser:
            return DRF_Response(
                data={
                    "response": "Вы не админ, чтобы создать супер пользователя"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer: CreateCustomUserSerializer = CreateCustomUserSerializer(
            data=request.data
        )

        new_password: Optional[str] = request.data.get("password", None)
        if not new_password or not isinstance(new_password, str):
            return DRF_Response(
                data={
                    "password": "Пароль обязан быть в формате строки"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        valid: bool = serializer.is_valid()
        if valid:
            if is_superuser:
                is_staff = True

            new_custom_user: CustomUser = serializer.save(
                is_superuser=is_superuser,
                is_staff=is_staff,
                password=new_password
            )
            new_custom_user.set_password(new_password)
            new_custom_user.save()
            refresh_token: RefreshToken = RefreshToken.for_user(
                new_custom_user
            )
            resulted_data: dict[str, Any] = serializer.data.copy()
            resulted_data.setdefault("refresh", str(refresh_token))
            resulted_data.setdefault("access", str(refresh_token.access_token))
            response: DRF_Response = DRF_Response(
                data=resulted_data,
                status=status.HTTP_201_CREATED
            )
            return response
        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["DELETE"],
        url_path="delete",
        detail=False,
        permission_classes=(IsAdminUser,)
    )
    def delete_users(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        user_ids: Optional[List[int]] = request.data.get("user_ids", None)
        if not user_ids:
            return DRF_Response(
                data={
                    "message": "user_ids должен быть предоставлен с id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        deleted_objs: int = 0
        deleted_objs = CustomUser.objects.get_not_deleted.filter(
            id__in=user_ids
        ).update(
            datetime_deleted=datetime.now()
        )
        msg: str = f"{deleted_objs} пользователей успешно удалено" \
            if deleted_objs > 0 else "Не один из пользователй не был удалён"

        return DRF_Response(
            data={
                "response": msg
            }
        )
