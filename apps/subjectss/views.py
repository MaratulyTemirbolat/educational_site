from typing import (
    Any,
    Tuple,
    Dict,
    Optional,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from django.db.models import (
    Manager,
    QuerySet,
)

from subjectss.models import GeneralSubject
from subjectss.serializers import GeneralSubjectBaseSerializer
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

    def get_obj_or_response(
        self,
        request: DRF_Request,
        pk: int | str,
        is_deleted: bool = False
    ) -> Tuple[GeneralSubject | DRF_Response, bool]:
        """Return object and boolean as True. Otherwise Response and False."""
        if is_deleted and not request.user.is_superuser:
            return (DRF_Response(
                data={
                    "message": "Вы не админ, чтобы получать удаленных юзеров"
                },
                status=status.HTTP_403_FORBIDDEN
            ), False)
        obj: Optional[GeneralSubject] = None
        obj = self.get_queryset_instance(
            class_name=GeneralSubject,
            queryset=self.get_queryset(),
            pk=pk
        )
        if not obj:
            return (DRF_Response(
                data={
                    "response": f"Объект с ID: {pk} не найден или удалён"
                },
                status=status.HTTP_404_NOT_FOUND
            ), False)
        return (obj, True)

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
            is_deleted=is_deleted
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
