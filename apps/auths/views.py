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
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)

from django.db.models import QuerySet
from django.contrib.auth import login

from abstracts.mixins import ModelInstanceMixin
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator
from auths.permissions import (
    IsNonDeletedUser,
    IsCustomAdminUser,
)
from auths.models import (
    CustomUser,
    CustomUserManager,
)
from auths.serializers import (
    CustomUserSerializer,
    DetailCustomUserSerializer,
    CreateCustomUserSerializer,
    CustomUserListStudentSerializer,
    CustomUserListTeacherSerializer,
    CustomUserLoginSerializer,
)
from auths.mixins import EmailObjectMixin
from teaching.permissions import IsTeacherOrUser


class CustomUserViewSet(
    EmailObjectMixin,
    ModelInstanceMixin,
    DRFResponseHandler,
    ViewSet
):
    """CustomUserViewSet."""

    queryset: CustomUserManager = CustomUser.objects
    permission_classes: tuple[Any] = (
        IsNonDeletedUser,
        IsCustomAdminUser,
    )
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator
    serializer_class: CustomUserSerializer = CustomUserSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[CustomUser]:
        """Get not deleted users."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

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
        pk: str | int,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Hadnle GET-request with provided id."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))
        is_custom_user: bool = False
        obj_response: CustomUser | DRF_Response
        obj_response, is_custom_user = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=CustomUser,
            queryset=self.get_queryset(
                is_deleted=is_deleted
            ).select_related(
                "student",
                "teacher",
                "teacher__subscription",
                "teacher__status_subscription",
            ),
            is_deleted=is_deleted
        )
        if is_custom_user:
            return self.get_drf_response(
                request=request,
                data=obj_response,
                serializer_class=DetailCustomUserSerializer
            )
        return obj_response

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

    @action(
        methods=["GET"],
        url_path="block",
        detail=True,
        permission_classes=(IsAdminUser,)
    )
    def block(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        user: Optional[CustomUser] = None
        user = self.get_queryset_instance(
            class_name=CustomUser,
            queryset=self.queryset.get_not_deleted(),
            pk=pk
        )
        if not user:
            return DRF_Response(
                data={
                    "message": f"Пользователь с {pk} не найден или удалён"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if not user.is_active:
            return DRF_Response(
                data={
                    "message": f"Пользователь {user} уже заблокирован"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.block()
        return DRF_Response(
            data={
                "message": f"Пользователь {user} успешно заблокирован"
            },
            status=status.HTTP_202_ACCEPTED
        )

    @action(
        methods=["GET"],
        url_path="unblock",
        detail=True,
        permission_classes=(IsAdminUser,)
    )
    def unblock(
        self,
        request: DRF_Request,
        pk: int = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        user: Optional[CustomUser] = None
        user = self.get_queryset_instance(
            class_name=CustomUser,
            queryset=self.queryset.get_not_deleted(),
            pk=pk
        )
        if not user:
            return DRF_Response(
                data={
                    "message": f"Пользователь с {pk} не найден или удалён"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if user.is_active:
            return DRF_Response(
                data={
                    "message": f"Пользователь {user} не заблокирован"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.unblock()
        return DRF_Response(
            data={
                "message": f"Пользователь {user} успешно разблокирован"
            },
            status=status.HTTP_202_ACCEPTED
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="students",
        url_name="get_students",
        permission_classes=(IsCustomAdminUser, IsTeacherOrUser,)
    )
    def get_students(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request on students to view the list."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))
        students: QuerySet[CustomUser] = self.get_queryset(
            is_deleted=is_deleted
        ).filter(student__isnull=False)\
            .select_related("student")
        return self.get_drf_response(
            request=request,
            data=students,
            serializer_class=CustomUserListStudentSerializer,
            many=True
        )

    # НЕ ОТИМИЗИРОВАН!!!
    @action(
        methods=["GET"],
        detail=False,
        url_path="teachers",
        url_name="get_teachers",
        permission_classes=(IsCustomAdminUser, IsAuthenticated,)
        # permission_classes=(AllowAny,)
    )
    def get_teachers(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain the list of user-teachers."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))
        teachers: QuerySet[CustomUser] = self.get_queryset(
            is_deleted=is_deleted
        ).filter(teacher__isnull=False).select_related(
            "teacher",
            "teacher__subscription",
            "teacher__status_subscription"
        )

        return self.get_drf_response(
            request=request,
            data=teachers,
            serializer_class=CustomUserListTeacherSerializer,
            many=True,
            paginator=self.pagination_class()
        )

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="recover",
        url_name="recover_user",
        permission_classes=(IsAdminUser,)
    )
    def recover(
        self,
        request: DRF_Request,
        pk: int | str,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Hadle GET, POST requests to recover the user if deleted."""

        user_response: DRF_Response | CustomUser
        is_user: bool = False
        user_response, is_user = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=CustomUser,
            queryset=self.get_queryset(is_deleted=True)
        )
        if is_user:
            user_response.recover()
            return self.get_drf_response(
                request=request,
                data=user_response,
                serializer_class=DetailCustomUserSerializer
            )
        msg: str = f"Пользователь с id: {pk} не существует или он не удалён"
        return DRF_Response(
            data={
                "response": msg
            },
            status=status.HTTP_404_NOT_FOUND
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=(AllowAny,)
    )
    def login(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle POST-request to login user."""

        serializer: CustomUserLoginSerializer = CustomUserLoginSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user: Optional[CustomUser] = self.get_user_by_email(
                email=request.data.get("email", "")
            )
            if not user:
                return DRF_Response(
                    data={"response": "Нет пользователя с таким 'email'"},
                    status=status.HTTP_404_NOT_FOUND
                )
            are_same: bool = user.check_password(
                raw_password=request.data.get("password", "")
            )
            if not are_same:
                return DRF_Response(
                    data={"response": "Ваш пароль не соостветствует"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not user.is_active:
                return DRF_Response(
                    data={"response": "Ваш аккаунт неактивный"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            login(request=request, user=user)
            refresh_token: RefreshToken = RefreshToken.for_user(user=user)
            det_ser: DetailCustomUserSerializer = DetailCustomUserSerializer(
                instance=user,
                many=False
            )
            resulted_data: dict[str, Any] = det_ser.data.copy()
            resulted_data.setdefault("refresh", str(refresh_token))
            resulted_data.setdefault("access", str(refresh_token.access_token))
            response: DRF_Response = DRF_Response(
                data=resulted_data,
                status=status.HTTP_200_OK
            )
            return response
        return DRF_Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
