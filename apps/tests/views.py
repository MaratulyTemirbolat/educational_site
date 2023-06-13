from typing import Any

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
)

from django.db.models import (
    Manager,
    QuerySet,
)

from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from abstracts.paginators import AbstractPageNumberPaginator
from tests.serializers import (
    QuizTypeBaseSerializer,
)
from tests.models import (
    QuizType,
)


class QuizTypeViewSet(
    ModelInstanceMixin,
    DRFResponseHandler,
    ViewSet
):
    """QuizTypeViewSet."""

    queryset: Manager = QuizType.objects
    permission_classes: tuple[Any] = (AllowAny,)
    pagination_class: AbstractPageNumberPaginator = \
        AbstractPageNumberPaginator
    serializer_class: QuizTypeBaseSerializer = QuizTypeBaseSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[QuizType]:
        """Get deleted/non-deleted chats."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request to get all quiz types."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))

        if is_deleted and not request.user.is_superuser:
            return DRF_Response(
                data={
                    "response": "Вы не можете запрашивать удалённые чаты"
                },
                status=HTTP_403_FORBIDDEN
            )

        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(is_deleted=is_deleted),
            many=True,
            serializer_class=self.serializer_class
        )
        return response
