from typing import (
    Any,
    Optional,
    Union,
)

from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from django.db.models import (
    Manager,
    QuerySet,
)

from abstracts.handlers import DRFResponseHandler
from abstracts.mixins import ModelInstanceMixin
from abstracts.paginators import AbstractPageNumberPaginator
from abstracts.tools import conver_to_int_or_none
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
    QuizQuestionViewModelSerializer,
    QuizQuestionAnswerCreateModelSerializer,
)
from tests.models import (
    QuizType,
    Quiz,
    QuizQuestionAnswer,
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
        quiz_resp: Union[Quiz, DRF_Response]
        quiz_resp, is_existed = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=Quiz,
            queryset=self.get_queryset().select_related(
                "quiz_type"
            ).prefetch_related(
                "quiz_questions__question",
                "quiz_questions__user_answer",
                "quiz_questions__question__answers",
                "attached_questions",
                "attached_questions__answers"
            )
        )
        if not is_existed:
            return quiz_resp
        provided_serializer: Union[
            QuizDetailModelSerializer,
            QuizQuestionViewModelSerializer
        ] = kwargs.get("create_serializer", QuizDetailModelSerializer)
        self.check_object_permissions(
            request=request,
            obj=quiz_resp
        )
        return self.get_drf_response(
            request=request,
            data=quiz_resp,
            serializer_class=provided_serializer
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
            new_quiz: Quiz = Quiz(
                name=request.data.get("name"),
                quiz_type_id=request.data.get("quiz_type"),
                student=request.user.student
            )
            new_quiz._subject_id: Optional[int] = conver_to_int_or_none(
                number=request.data.get("subject_id", "")
            )
            new_quiz._class_number: Optional[int] = conver_to_int_or_none(
                number=request.data.get("class_number", "")
            )
            new_quiz._topic_id: Optional[int] = conver_to_int_or_none(
                number=request.data.get("topic_id", "")
            )
            new_quiz.save()
            return self.retrieve(
                request=request,
                pk=new_quiz.id,
                create_serializer=QuizQuestionViewModelSerializer
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
        url_path="upload_answers"
    )
    def upload_quiz(
        self,
        request: DRF_Request,
        pk: int,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> DRF_Response:
        """Handle POST-request to upload new quiz."""

        is_existed: bool = False
        quiz_resp: Union[Quiz, DRF_Response]
        quiz_resp, is_existed = self.get_obj_or_response(
            request=request,
            pk=pk,
            class_name=Quiz,
            queryset=self.get_queryset().select_related(
                "quiz_type"
            ).prefetch_related(
                "quiz_questions__question",
                "quiz_questions__user_answer",
                "quiz_questions__question__answers",
                "attached_questions",
                "attached_questions__answers"
            )
        )
        if not is_existed:
            return quiz_resp
        self.check_object_permissions(
            request=request,
            obj=quiz_resp
        )
        user_answers: list[dict[str, int]] = request.data.get(
            "questions", []
        )
        quiz_questions_number: int = quiz_resp.attached_questions.count()
        if len(user_answers) != quiz_questions_number:
            message: str = "Количество ответов не равно количеству вопросов"
            return DRF_Response(
                data={
                    "response": message
                },
                status=HTTP_400_BAD_REQUEST
            )
        if quiz_resp.quiz_questions.count() > 0:
            return DRF_Response(
                data={
                    "response": "Тест завершен. Загружать ответы нельзя."
                },
                status=HTTP_400_BAD_REQUEST
            )
        serializer: QuizQuestionAnswerCreateModelSerializer = \
            QuizQuestionAnswerCreateModelSerializer

        user_answ: dict[str, int]
        for user_answ in user_answers:
            if quiz_resp.id != user_answ["quiz"]:
                message: str = "Номер теста в вопросе с \
id: {0} не совпадает с запрошенным тестом {1}".format(
                        user_answ['question'],
                        quiz_resp.id
                    )
                breakpoint()
                return DRF_Response(
                    data={
                        "response": message
                    },
                    status=HTTP_400_BAD_REQUEST
                )
            serializer = QuizQuestionAnswerCreateModelSerializer(
                data=user_answ
            )
            if not serializer.is_valid():
                return DRF_Response(
                    data={
                        "response": "Ошибка в \
тесте: {0}, вопросе: {1}, ответе: {2}".format(
                            user_answ["quiz"],
                            user_answ["question"],
                            user_answ["user_answer"]
                        ),
                        "errors": serializer.errors
                    },
                    status=HTTP_400_BAD_REQUEST
                )
        quiz_question_answers_list: list[QuizQuestionAnswer] = []
        user_answ: dict[str, int]
        for user_answ in user_answers:
            quiz_question_answers_list.append(
                QuizQuestionAnswer(
                    quiz_id=user_answ["quiz"],
                    question_id=user_answ["question"],
                    user_answer_id=user_answ["user_answer"]
                )
            )
        QuizQuestionAnswer.objects.bulk_create(objs=quiz_question_answers_list)
        return DRF_Response(
            data={
                "response": "Данные успешно сохранены"
            },
            status=HTTP_200_OK
        )
