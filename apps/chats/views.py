# from django.shortcuts import render
from typing import Any

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)

from django.db.models import (
    Manager,
    QuerySet,
    Q,
)

from abstracts.mixins import ModelInstanceMixin
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator
from chats.models import (
    PersonalChat,
    Message,
)
from chats.serializers import (
    PersonalChatBaseModelSerializer,
    PersonalChatListSerializer,
    PersonalChatDetailSerializer,
    MessageCreateModelSerializer,
    MessageBaseModelSerializer,
)
from chats.permissions import IsChatMember
from auths.permissions import IsNonDeletedUser


class PersonalChatViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """PersonalChatViewSet."""

    queryset: Manager = PersonalChat.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser, IsChatMember,)
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator
    serializer_class: PersonalChatBaseModelSerializer = \
        PersonalChatBaseModelSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[PersonalChat]:
        """Get not deleted chats."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain non_deleted chats."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))

        if is_deleted and not request.user.issuperuser:
            return DRF_Response(
                data={
                    "response": "Вы не можете запрашивать удалённые чаты"
                },
                status=HTTP_403_FORBIDDEN
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(is_deleted=is_deleted).filter(
                Q(student__user=request.user) | Q(teacher__user=request.user)
            ).select_related(
                "student",
                "teacher",
                "student__user",
                "teacher__user"
            ),
            serializer_class=PersonalChatListSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int,
        *args: tuple[Any],
        **kwargs: dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request with provided id chat."""
        res_chat: PersonalChat | DRF_Response
        is_existed: bool = False
        res_chat, is_existed = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=PersonalChat,
            queryset=self.get_queryset().select_related(
                "student",
                "teacher",
                "student__user",
                "teacher__user",
            )
        )
        if not is_existed:
            return res_chat
        self.check_object_permissions(
            request=request,
            obj=res_chat
        )
        return self.get_drf_response(
            request=request,
            data=res_chat,
            serializer_class=PersonalChatDetailSerializer
        )

    def create(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Hadle POST-request to create a new chat."""

        serializer: PersonalChatBaseModelSerializer = self.serializer_class(
            data=request.data
        )
        valid: bool = serializer.is_valid()
        if valid:
            teacher_id: int = request.data.get("teacher")
            student_id: int = request.data.get("student")

            if teacher_id == student_id:
                return DRF_Response(
                    data={"response": "Нельзя отправлять одинаковые id"},
                    status=HTTP_400_BAD_REQUEST
                )
            if PersonalChat.objects.filter(
                student_id=student_id,
                teacher_id=teacher_id
            ).exists():
                return DRF_Response(
                    data={"response": "Данный чат уже существует"},
                    status=HTTP_400_BAD_REQUEST
                )
            new_chat: PersonalChat = serializer.save()
            return self.get_drf_response(
                request=request,
                data=new_chat,
                serializer_class=PersonalChatListSerializer
            )
        return DRF_Response(
            data={
                "response": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="add_message",
        permission_classes=(IsNonDeletedUser, IsChatMember,)
    )
    def add_message(
        self,
        request: DRF_Request,
        pk: int,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Add message to the specific chat."""
        res_chat: PersonalChat | DRF_Response
        is_existed: bool = False
        res_chat, is_existed = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=PersonalChat,
            queryset=self.get_queryset()
        )
        if not is_existed:
            return res_chat

        self.check_object_permissions(
            request=request,
            obj=res_chat
        )
        serializer: MessageCreateModelSerializer = \
            MessageCreateModelSerializer(
                data=request.data,
                context={"request": request, "to_chat": res_chat}
            )
        valid: bool = serializer.is_valid()
        if valid:
            new_message: Message = serializer.save()
            return self.get_drf_response(
                request=request,
                data=new_message,
                serializer_class=MessageBaseModelSerializer
            )
        return DRF_Response(
            data={
                "response": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )


# def index(request):
#     return render(request=request, template_name='chat/index.html')
