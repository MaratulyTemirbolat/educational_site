# from django.shortcuts import render
from typing import Any

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)

from django.db.models import (
    Manager,
    QuerySet,
    Q,
)

from abstracts.mixins import ModelInstanceMixin
from abstracts.handlers import DRFResponseHandler
from abstracts.paginators import AbstractPageNumberPaginator

from chats.models import PersonalChat
from chats.serializers import (
    PersonalChatBaseModelSerializer,
    PersonalChatListSerializer,
)
from auths.permissions import IsNonDeletedUser


class PersonalChatViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """PersonalChatViewSet."""

    queryset: Manager = PersonalChat.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser,)
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
            ),
            serializer_class=PersonalChatListSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

# def index(request):
#     return render(request=request, template_name='chat/index.html')
