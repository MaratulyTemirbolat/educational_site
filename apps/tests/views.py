from typing import (
    Any,
    Optional,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
)

from django.db.models import (
    Manager,
    QuerySet,
)

from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from abstracts.paginators import AbstractPageNumberPaginator
from auths.permissions import IsNonDeletedUser
from subjectss.permissions import IsStudent
from subjectss.models import Student
from tests.permissions import IsQuizStudent
from tests.serializers import (
    QuizTypeBaseSerializer,
    QuizBaseModelSerializer,
    QuizListModelSerializer,
    QuizDetailModelSerializer,
    QuizCreateModelSeriazizer,
)
from tests.models import (
    QuizType,
    Quiz,
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


class QuizViewSet(
    ModelInstanceMixin,
    DRFResponseHandler,
    ViewSet
):
    """QuizViewSet."""

    queryset: Manager = Quiz.objects
    permission_classes: tuple[Any] = (
        IsAuthenticated,
        IsNonDeletedUser,
        IsStudent,
        IsQuizStudent,
    )
    serializer_class: QuizBaseModelSerializer = QuizBaseModelSerializer
    pagination_class: AbstractPageNumberPaginator = AbstractPageNumberPaginator

    def get_queryset(self, student_id: Optional[int] = None) -> QuerySet[Quiz]:
        """Get queryset of the Quizes."""
        return self.queryset.filter(
            student_id=student_id
        ) if student_id else self.queryset.all()

    def list(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request to obtain user's quizes."""
        student_id: int = Student.objects.filter(
            user_id=request.user.id
        ).values_list("id", flat=True).first()
        response: DRF_Response = self.get_drf_response(
            request=request,
            data=self.get_queryset(
                student_id=student_id
            ).select_related(
                "quiz_type"
            ),
            serializer_class=QuizListModelSerializer,
            many=True,
            paginator=self.pagination_class()
        )
        return response

    def retrieve(
        self,
        request: DRF_Request,
        pk: int,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle GET-request with specified id."""
        is_existed: bool = False
        quiz_resp: Quiz | DRF_Response
        quiz_resp, is_existed = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=Quiz,
            queryset=self.get_queryset().select_related(
                "quiz_type"
            ).prefetch_related(
                "quiz_questions__question",
                "quiz_questions__user_answer",
            )
        )
        if not is_existed:
            return quiz_resp
        self.check_object_permissions(
            request=request,
            obj=quiz_resp
        )
        return self.get_drf_response(
            request=request,
            data=quiz_resp,
            serializer_class=QuizDetailModelSerializer
        )

    def create(
        self,
        request: DRF_Request,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle POST-request to get new generated quiz by type."""

        serializer: QuizCreateModelSeriazizer = QuizCreateModelSeriazizer(
            data=request.data,
            context={"request": request, "student": request.user.student}
        )
        valid: bool = serializer.is_valid()
        if valid:
            new_quiz: Quiz = serializer.save()
            return self.get_drf_response(
                request=request,
                data=new_quiz,
                serializer_class=QuizListModelSerializer
            )
        return DRF_Response(
            data={
                "response": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )
