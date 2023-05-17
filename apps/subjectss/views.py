from typing import (
    Any,
    Tuple,
    Dict,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from django.db.models import (
    Manager,
    QuerySet,
)

from subjectss.models import (
    GeneralSubject,
    TrackWay,
)
from subjectss.serializers import (
    GeneralSubjectBaseSerializer,

    TrackWayBaseSerializer,
    TrackWayDetailSerializer,
)
from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from abstracts.paginators import AbstractPageNumberPaginator
from auths.permissions import IsNonDeletedUser


class GeneralSubjectViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """GeneralSubjectViewSet."""

    queryset: Manager = GeneralSubject.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser,)
    serializer_class: GeneralSubjectBaseSerializer = \
        GeneralSubjectBaseSerializer
    pagination_class: AbstractPageNumberPaginator = AbstractPageNumberPaginator

    def get_queryset(
        self,
        is_deleted: bool = False
    ) -> QuerySet[GeneralSubject]:
        """Get queryset by is_deleted state."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request for all subjects."""
        is_deleted: bool = request.GET.get("is_deleted", False)
        if is_deleted and not request.user.is_superuser:
            message: str = "Вам нельзя запрашивать удалённых пользователей"
            return DRF_Response(
                data={
                    "response": message
                },
                status=status.HTTP_403_FORBIDDEN
            )
        sear_queryset: QuerySet[GeneralSubject] = self.queryset.get_deleted() \
            if is_deleted else self.get_queryset()
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=sear_queryset,
            serializer_class=GeneralSubjectBaseSerializer,
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
        """Handle GET-request to find GeneralSubject with provided id."""
        is_deleted: bool = request.GET.get("is_deleted", False)
        obj_response: GeneralSubject | DRF_Response
        is_user: bool = False
        obj_response, is_user = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=GeneralSubject,
            is_deleted=is_deleted,
            queryset=self.get_queryset(is_deleted=is_deleted)
        )
        if is_user:
            return DRF_Response(
                data={
                    "response": GeneralSubjectBaseSerializer(
                        instance=obj_response
                    ).data
                },
                status=status.HTTP_200_OK
            )
        return obj_response


class TrackWayViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """TrackWayViewSet."""

    queryset: Manager = TrackWay.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser,)
    pagination_class: AbstractPageNumberPaginator = AbstractPageNumberPaginator
    serializer_class: TrackWayBaseSerializer = TrackWayBaseSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[TrackWay]:
        """Get queryset of Trackways by provided is_deletede property."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain all records."""
        is_deleted: bool = request.GET.get("is_deleted", False)
        if is_deleted and request.user.is_superuser:
            return DRF_Response(
                data={
                    "message": "Не Админ, чтобы запрашивать удалённые данные"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return self.get_drf_response(
            request=request,
            data=self.get_queryset(is_deleted=is_deleted),
            serializer_class=self.serializer_class,
            many=True,
            paginator=self.pagination_class()
        )

    def retrieve(
        self,
        request: DRF_Request,
        pk: str,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to find GeneralSubject with provided id."""
        is_deleted: bool = request.GET.get("is_deleted", False)
        obj_response: TrackWay | DRF_Response
        is_obj: bool = False
        obj_response, is_obj = self.get_obj_or_response(
            request=request,
            pk=pk,
            is_deleted=is_deleted,
            class_name=TrackWay,
            queryset=self.get_queryset(
                is_deleted=is_deleted
            ).prefetch_related("subjects")
        )
        if is_obj:
            return DRF_Response(
                data={
                    "response": TrackWayDetailSerializer(
                        instance=obj_response
                    ).data
                },
                status=status.HTTP_200_OK
            )
        return obj_response
