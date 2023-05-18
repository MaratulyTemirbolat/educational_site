from typing import (
    Any,
    Tuple,
    Dict,
    Optional,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)

from django.db.models import (
    Manager,
    QuerySet,
)

from subjectss.models import (
    GeneralSubject,
    TrackWay,
    Class,

    ClassSubject,
    ClassSubjectQuerySet,
)
from subjectss.serializers import (
    GeneralSubjectBaseSerializer,

    TrackWayBaseSerializer,
    TrackWayDetailSerializer,

    ClassBaseSerializer,

    ClassSubjectBaseSerializer,
    ClassSubjectDetailSerializer,
)
from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from abstracts.paginators import AbstractPageNumberPaginator
from auths.permissions import IsNonDeletedUser
from abstracts.tools import conver_to_int_or_none


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
                status=HTTP_403_FORBIDDEN
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
                status=HTTP_200_OK
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
                status=HTTP_403_FORBIDDEN
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
                status=HTTP_200_OK
            )
        return obj_response


class ClassViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """ClassViewSet."""

    queryset: Manager = Class.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser,)
    pagination_class: AbstractPageNumberPaginator = AbstractPageNumberPaginator
    serializer_class: ClassBaseSerializer = ClassBaseSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[Class]:
        """Get queryset of Classes by provided is_deletede property."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to get the list of classes."""

        is_deleted: bool = request.GET.get("is_deleted", False)
        if is_deleted and not request.user.is_superuser:
            return DRF_Response(
                data={
                    "response": "Вы не админ, чтобы запрашивать удалённых"
                },
                status=HTTP_403_FORBIDDEN
            )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(is_deleted=is_deleted),
            serializer_class=self.serializer_class,
            many=True
        )
        return response


class ClassSubjectViewSet(ModelInstanceMixin, DRFResponseHandler, ViewSet):
    """ClassSubjectViewSet."""

    queryset: Manager = ClassSubject.objects
    permission_classes: tuple[Any] = (IsNonDeletedUser,)
    class_serializer: ClassSubjectBaseSerializer = ClassSubjectBaseSerializer

    def get_queryset(self, is_deleted: bool = False) -> QuerySet[ClassSubject]:
        """Get queryset of ClassSubjects by provided is_deletede property."""
        return self.queryset.get_deleted() \
            if is_deleted else self.queryset.get_not_deleted()

    def list(
        self,
        request: DRF_Request,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain the list of ClassSubjects."""
        is_deleted: bool = bool(request.query_params.get("is_deleted", False))
        general_subject_id: Optional[int] = conver_to_int_or_none(
            number=request.query_params.get("subject_id", "")
        )
        attached_class_id: Optional[int] = conver_to_int_or_none(
            number=request.query_params.get("class_id", "")
        )
        if is_deleted and not request.user.is_superuser:
            return DRF_Response(
                data={
                    "message": "Вы не админ, чтобы брать удалённые данные"
                },
                status=HTTP_403_FORBIDDEN
            )
        search_queryset: ClassSubjectQuerySet[ClassSubject] = \
            self.get_queryset(is_deleted=is_deleted)

        if general_subject_id or attached_class_id:
            search_queryset = search_queryset.get_class_subject(
                attached_class_id=attached_class_id,
                general_subject_id=general_subject_id
            )
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=search_queryset.select_related(
                "attached_class",
                "general_subject"
            ),
            serializer_class=self.class_serializer,
            many=True
        )
        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int | str = 0,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain specific ClassSubject obj."""
        is_deleted: bool = request.query_params.get("is_deleted", False)
        is_class_subject: bool = False
        obj_response: ClassSubject | DRF_Response 
        obj_response, is_class_subject = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=ClassSubject,
            queryset=self.get_queryset(
                is_deleted=is_deleted
            ).select_related(
                "general_subject",
                "attached_class"
            ),
            is_deleted=is_deleted
        )

        if is_class_subject:
            return self.get_drf_response(
                request=request,
                data=obj_response,
                serializer_class=ClassSubjectDetailSerializer
            )
        return obj_response
