from datetime import datetime
from typing import (
    Optional,
    Any,
)
from random import choice

from django.core.management.base import BaseCommand

from tests.models import (
    QuizType,
    Question,
    Answer,
    Quiz,
    QuizQuestionAnswer,
)
from subjectss.models import (
    Topic,
    Student,
)


class Command(BaseCommand):
    """Custom command for filling up database."""
    QUIZ_NAME_TYPES = (
        "предмет",
        "тема",
        "класс",
    )
    QUIZ_QUESTIONS_NUMBER = {
        "предмет": 20,
        "класс": 10,
        "тема": 5
    }

    __answers_template: tuple[str] = (
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "Hello", "Russia", "Kazakhstan", "Andrew",
        "Germany", "Turkey", "Europe", "Asia", "World",
        "Mouse", "God", "Cat", "Phone", "Apple", "Android",
        "Django", "Python", "Golang", "React", "Angular",
        "JavaScript", "Java", "Number", "NaN", "String",
        "Boolean", "Double", "Float", "Type", "Keyboard",
        "Dirol", "Orbit", "Samsung", "LG", "Sony", "Asus",
        "Dell", "Lenovo", "Bag", "Screen", "C++", "C#",
        "Vue", "a", "b", "c", "d", "e", "f", "g", "h", "i",
        "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z", "America", "Canada", "Germany",
        "France", "Italy",
    )
    __answers_number: tuple[int] = (4, 7,)

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def generate_quiz_types(self) -> None:
        """Generate test quiz types in local db."""
        created_cnt: int = 0
        is_created: bool = False
        _: QuizType

        quiz_type: str = ""
        for quiz_type in self.QUIZ_NAME_TYPES:
            _, is_created = QuizType.objects.get_or_create(name=quiz_type)
            created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} типов тестов успешно создано и добавлено")

    def generate_questions(self, required_number: int = 0) -> None:
        """Generate test answers in local db."""
        def get_name(i: int) -> str:
            return f"Вопрос №{i}"
        all_topic_ids: tuple[int] = tuple(
            Topic.objects.values_list("id", flat=True)
        )
        created_cnt: int = 0
        _: Optional[Question] = None
        is_existed: bool = False
        name: str = ""
        topic_id: int = 0

        i: int
        for i in range(required_number):
            name = get_name(i)
            topic_id = choice(all_topic_ids)
            is_existed = Question.objects.filter(
                name=name
            ).exists()
            if not is_existed:
                Question.objects.create(
                    name=name,
                    attached_subject_class_id=topic_id
                )
                created_cnt += 1

        print(f"{created_cnt} вопросов успешно создано и добавлено")

    def generate_answers(self) -> None:
        """Generate test answers for local db."""
        questions_id: tuple[int] = tuple(
            Question.objects.values_list("id", flat=True)
        )
        is_correct: tuple[bool] = (True, False,)
        is_existed: bool = False
        name: str = ""
        answers_number: int = 0
        created_number: int = 0

        question_id: int
        for question_id in questions_id:
            answers_number = choice(self.__answers_number)
            _: int
            for _ in range(answers_number):
                name = choice(self.__answers_template)
                is_existed = Answer.objects.filter(
                    name=name,
                    question_id=question_id
                ).exists()
                if not is_existed:
                    Answer.objects.create(
                        name=name,
                        question_id=question_id,
                        is_correct=choice(is_correct)
                    )
                    created_number += 1
        print(f"{created_number} ответов успешно создано и добавлено в базу")

    def generate_quizes(self, required_number: int = 0) -> None:
        def get_questions_number(quiz_type: str = "") -> int:
            return self.QUIZ_QUESTIONS_NUMBER.get(quiz_type, 0)
        all_students: tuple[int] = tuple(
            Student.objects.values_list("id", flat=True)
        )
        all_quiz_types: tuple[QuizType] = tuple(
            QuizType.objects.all()
        )
        all_questions: tuple[Question] = tuple(
            Question.objects.all()
        )
        quiz: Optional[Quiz] = None
        quiz_type: Optional[QuizType] = None
        all_quizes: list[Quiz] = []
        created_quizes: int = 0

        _: int
        for _ in range(required_number):
            quiz_type = choice(all_quiz_types)
            quiz = Quiz(
                student_id=choice(all_students),
                quiz_type=quiz_type
            )
            all_quizes.append(quiz)
            created_quizes += 1
        Quiz.objects.bulk_create(all_quizes)

        cur_question: Question = choice(all_questions)
        user_answer: Answer = choice(cur_question.answers.all())
        created_quiz_answers: int = 0
        correct_answers_number: int = 0
        is_existed_user_quest_answ: bool = False
        quiz: Quiz
        for quiz in all_quizes:
            question_number: int = get_questions_number(quiz.quiz_type.name)
            correct_answers_number = 0
            _: int
            for _ in range(question_number):
                cur_question = choice(all_questions)
                user_answer = choice(cur_question.answers.all())
                is_existed_user_quest_answ = QuizQuestionAnswer.objects.filter(
                    quiz_id=quiz.id,
                    question_id=cur_question.id,
                    user_answer=user_answer.id
                ).exists()
                if not is_existed_user_quest_answ:
                    QuizQuestionAnswer.objects.create(
                        quiz=quiz,
                        question=cur_question,
                        user_answer=user_answer,
                        answer_point=1 if user_answer.is_correct else 0
                    )
                    correct_answers_number = correct_answers_number + 1 \
                        if user_answer.is_correct else correct_answers_number
                    created_quiz_answers += 1
            quiz.correct_answers = correct_answers_number

        print(f"{created_quizes} тестов успешно создано")
        print(f"{created_quiz_answers} ответов на тесты успешно создано")

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # Data generation
        self.generate_quiz_types()
        self.generate_questions(100)
        self.generate_answers()
        self.generate_quizes(50)

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
