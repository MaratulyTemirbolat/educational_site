from typing import (
    Any,
    Union,
)

from rest_framework.serializers import (
    ModelSerializer,
    DateTimeField,
    SerializerMethodField,
    HiddenField,
)

from abstracts.serializers import AbstractDateTimeSerializer
from tests.models import (
    QuizType,
    Quiz,
    Question,
    QuizQuestionAnswer,
    Answer,
)


class CurrentStudentSerializer:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['student']

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class AnswerForeignModelSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """AnswerForeignModelSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: Answer = Answer
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "is_correct",
            "question",
            "is_deleted",
            "datetime_created",
        )


class QuizTypeBaseSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """QuizTypeBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created

    class Meta:
        """Customization of the Serializer."""

        model: QuizType = QuizType
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "is_deleted",
            "datetime_created",
        )


class QuestionForeignModelSerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """QuestionBaseSerializer."""

    is_deleted: SerializerMethodField = AbstractDateTimeSerializer.is_deleted
    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    answers: AnswerForeignModelSerializer = AnswerForeignModelSerializer(
        many=True
    )

    class Meta:
        """Customization of the Serializer."""

        model: Question = Question
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "attached_subject_class",
            "is_deleted",
            "datetime_created",
            "answers",
        )


class QuizBaseModelSerializer(ModelSerializer):
    """QuizBaseModelSerializer."""

    datetime_created: DateTimeField = DateTimeField(
        format="%Y-%m-%d %H:%M",
        read_only=True
    )

    class Meta:
        """Customization of the serializer."""

        model: Quiz = Quiz
        fields: Union[tuple[str], str] = "__all__"


class QuizQuestionAnswerForeignSerializer(ModelSerializer):
    """QuizQuestionAnswerForeignSerializer."""

    question: QuestionForeignModelSerializer = QuestionForeignModelSerializer()
    user_answer: AnswerForeignModelSerializer = AnswerForeignModelSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: QuizQuestionAnswer = QuizQuestionAnswer
        fields: Union[tuple[str], str] = (
            "id",
            "quiz",
            "question",
            "user_answer",
        )


class QuizListModelSerializer(QuizBaseModelSerializer):
    """QuizListModelSerializer."""

    quiz_type: QuizTypeBaseSerializer = QuizTypeBaseSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Quiz = Quiz
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "quiz_type",
            "student",
            "datetime_created",
        )


class QuizDetailModelSerializer(QuizBaseModelSerializer):
    """QuizDetailModelSerializer."""

    quiz_type: QuizTypeBaseSerializer = QuizTypeBaseSerializer()
    quiz_questions: QuizQuestionAnswerForeignSerializer = \
        QuizQuestionAnswerForeignSerializer(
            many=True
        )
    correct_questions: SerializerMethodField = SerializerMethodField(
        method_name="get_correct_questions_number",
    )

    class Meta:
        """Customization of the Serializer."""

        model: Quiz = Quiz
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "quiz_type",
            "student",
            "quiz_questions",
            "datetime_created",
            "correct_questions",
        )

    def get_correct_questions_number(
        self,
        obj: Quiz,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> int:
        """Get correct number of questions."""
        return obj.quiz_questions.filter(
            user_answer__is_correct=True
        ).count()


class QuizCreateModelSeriazizer(ModelSerializer):
    """QuizCreateModelSeriazizer."""

    student: HiddenField = HiddenField(
        default=CurrentStudentSerializer()
    )

    class Meta:
        """Customization of the Serializer."""

        model: Quiz = Quiz
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "student",
            "quiz_type",
        )


class QuizQuestionViewModelSerializer(QuizBaseModelSerializer):
    """QuizQuestionViewModelSerializer."""

    quiz_type: QuizTypeBaseSerializer = QuizTypeBaseSerializer()
    attached_questions: QuestionForeignModelSerializer = \
        QuestionForeignModelSerializer(
            many=True
        )

    class Meta:
        """Customization of the Serializer."""

        model: Quiz = Quiz
        fields: Union[tuple[str], str] = (
            "id",
            "name",
            "student",
            "quiz_type",
            "datetime_created",
            "attached_questions",
        )


class QuizQuestionAnswerCreateModelSerializer(
    ModelSerializer
):
    """QuizQuestionAnswerCreateSerializer."""

    class Meta:
        """Customization of the Table."""

        model: QuizQuestionAnswer = QuizQuestionAnswer
        fields: Union[tuple[str], str] = (
            "quiz",
            "question",
            "user_answer",
        )
