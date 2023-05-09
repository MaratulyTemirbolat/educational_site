from datetime import datetime
from random import (
    randint,
    sample,
    choice,
)
from typing import (
    Any,
    Tuple,
    Dict,
)

from django.core.management.base import BaseCommand

from subjectss.models import (
    StudentSubjectState,
    GeneralSubject,
    Class,
    ClassSubject,
    Topic,
    TrackWay,
    Student,
    StudentRegisteredSubjects,
)
from auths.models import CustomUser


class Command(BaseCommand):
    """Custom command for filling up database."""

    CLASSES_LIMIT = 11
    GENERAL_SUBJECTS = (
        "Математика",
        "Физика",
        "Биология",
        "Химия",
        "Геометрия",
        "История",
        "Информатика",
        "Казахский",
        "Критическое мышление",
        "География",
        "Самопознание",
    )
    STUDENT_SUBJECT_STATES = (
        "Активный",
        "Закрытый",
        "Заброшен",
        "Завален",
        "Заблокирован",
    )
    EDU_VIDEO_URLS = (
        "https://www.youtube.com/watch?v=S3ZGcFDp4RM&t=1475s",
        "https://www.youtube.com/watch?v=-6DWwR_R4Xk",
        "https://www.youtube.com/watch?v=NErrGZ64OdE",
        "https://www.youtube.com/watch?v=OToyoIqVPQI",
        "https://www.youtube.com/watch?v=JXI2CsT2ZZQ",
        "https://www.youtube.com/watch?v=X85soC5evw0",
        "https://www.youtube.com/watch?v=S0e_5a2WB60",
        "https://www.youtube.com/watch?v=ANj7qUgzNq4",
    )
    __message_template_parts: Tuple[str] = (
        "hello", "world", "animal", "person",
        "good", "thank you", "nice", "show", "say",
        "anime", "Turkey", "Canada", "Kazakhstan", "dear",
        "bird", "dog", "cat", "queen", "buy", "sir", "apple",
        "pear", "zebra", "man", "girl", "boy", "Russia",
        "Paris", "United Kingdom", "boyfriend", "girlfriend",
        "Kaneki", "John", "Temirbolat", "Mike", "Marat", "Rem",
        "Ram", "laptop", "computer", "mouse", "lorem impsum",
        "Almaty", "Moscow", "Astana", "Karaganda", "NU", "KBTU",
        "or", "and", "as well as", "along with", "while", "including",
    )
    __student_states: tuple[bool] = (True, False,)

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def generate_classes(self) -> None:
        """Generate all test classes in db."""
        _: Class
        is_created: bool = False
        created_cnt: int = 0

        i: int
        for i in range(self.CLASSES_LIMIT):
            _, is_created = Class.objects.get_or_create(number=i+1)
            if is_created:
                created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} классов было успешно добавлено в базу")

    def generate_general_subjects(self) -> None:
        """Generate all test subjects in db."""
        _: GeneralSubject
        is_created: bool = False
        created_subj_cnt: int = 0
        subj_name: str
        for subj_name in self.GENERAL_SUBJECTS:
            _, is_created = GeneralSubject.objects.get_or_create(
                name=subj_name
            )
            if is_created:
                created_subj_cnt += 1
        print(f"{created_subj_cnt} предметов успешно создано")

    def generate_student_subj_states(self) -> None:
        """Generate all test student subject states for local db."""
        _: StudentSubjectState
        is_created: bool = False
        created_states: int = 0

        state_name: str
        for state_name in self.STUDENT_SUBJECT_STATES:
            _, is_created = StudentSubjectState.objects.get_or_create(
                name=state_name
            )
            if is_created:
                created_states += 1
        print(f"{created_states} состояний было успешно создано")

    def generate_class_subjects(self) -> None:
        """Generate all test subjects for the corresponded class."""
        def get_name(subj_name: str, class_name: str) -> str:
            return f"{subj_name} для {class_name} класса"

        all_subjects: tuple[tuple[int, str]] = tuple(
            GeneralSubject.objects.values_list("id", "name")
        )
        all_classes: tuple[tuple[int, int]] = tuple(
            Class.objects.values_list("id", "number")
        )

        _: ClassSubject
        is_created: bool = False
        created_cnt: int = 0

        subj_tuple: tuple[int, str]
        class_tuple: tuple[int, int]
        for subj_tuple in all_subjects:
            for class_tuple in all_classes:
                _, is_created = ClassSubject.objects.get_or_create(
                    name=get_name(
                        subj_name=subj_tuple[1],
                        class_name=class_tuple[1]
                    ),
                    general_subject_id=subj_tuple[0],
                    attached_class_id=class_tuple[0]
                )
                if is_created:
                    created_cnt += 1
        print(f"{created_cnt} Предметов по классам были создано успешно")

    def generate_topics(self, required_number: int = 0) -> None:
        """Generate all test topics for local db."""
        MIN_CONTENT_WORDS_NUM = 5
        MAX_CONTENT_WORDS_NUM = 30

        def get_random_content(subj_name: str) -> str:
            ran_words_number: int = randint(
                a=MIN_CONTENT_WORDS_NUM,
                b=MAX_CONTENT_WORDS_NUM
            )
            return f"'{subj_name.capitalize()}' контент: " + " ".join(
                sample(
                    population=self.__message_template_parts,
                    k=ran_words_number
                )
            )

        def get_topic_name(subject_name: str, index: int) -> str:
            return f"Тема {index} для предмета '{subject_name}'"

        all_subjects: tuple[tuple[int, str]] = tuple(
            GeneralSubject.objects.values_list(
                "id",
                "name"
            )
        )
        _: Topic
        is_created: bool = False
        created_cnt: int = 0

        i: int
        subj_tuple: tuple[int, str]
        for subj_tuple in all_subjects:
            for i in range(required_number):
                _, is_created = Topic.objects.get_or_create(
                    name=get_topic_name(subject_name=subj_tuple[1], index=i),
                    content=get_random_content(subj_name=subj_tuple[1]),
                    video_url=choice(self.EDU_VIDEO_URLS),
                    attached_subect_class_id=subj_tuple[0]
                )
                if is_created:
                    created_cnt += 1
        print(f"{created_cnt} тем успешно создано и добавлено в базу")

    def generate_trackways(self) -> None:
        """Generate test trackways in db."""
        trackways: tuple[str] = ("ЕНТ",)
        subjects: tuple[GeneralSubject] = tuple(GeneralSubject.objects.all())

        obj: TrackWay
        is_created: bool = False
        created_cnt: int = 0

        track: str
        for track in trackways:
            obj, is_created = TrackWay.objects.get_or_create(name=track)
            if is_created:
                subj: GeneralSubject
                for subj in sample(population=subjects, k=5):
                    obj.subjects.add(subj)
                    created_cnt += 1
        print(f"{created_cnt} предметов по направлению успешно создано")

    def generate_students(self) -> None:
        """Generate all test Students among all CustomUsers."""
        all_users_ids: tuple[int] = tuple(CustomUser.objects.values_list(
            "id",
            flat=True
        ))

        created_cnt: int = 0
        is_created: bool = False
        points_number: int = 0
        _: Student
        is_existed: bool = False

        is_stud: bool = False
        user_id: int
        for user_id in all_users_ids:
            is_stud = choice(self.__student_states)
            is_existed = Student.objects.filter(user_id=user_id).exists()
            if is_stud and not is_existed:
                points_number = randint(0, 10000)  # Исправить get_or_create
                _, is_created = Student.objects.get_or_create(
                    user_id=user_id,
                    points=points_number
                )
                created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} студент(ов) успешно создано и добавлено")

    def generate_student_registered_subjects(
        self,
        required_number: int = 0
    ) -> None:
        """Register test users with all subjects."""
        student_ids: tuple[int] = tuple(
            Student.objects.values_list("id", flat=True)
        )
        class_subject_ids: tuple[int] = tuple(
            ClassSubject.objects.values_list("id", flat=True)
        )
        all_state_ids: tuple[int] = tuple(
            StudentSubjectState.objects.values_list("id", flat=True)
        )

        _: StudentRegisteredSubjects
        is_existed: bool = False
        created_cnt: int = 0
        student_id: int = 0
        class_subject_id: int = 0

        i: int
        for i in range(required_number):
            student_id = choice(student_ids)
            class_subject_id = choice(class_subject_ids)
            is_existed = StudentRegisteredSubjects.objects.filter(
                student_id=student_id,
                class_subject_id=class_subject_id
            ).exists()
            if not is_existed:
                StudentRegisteredSubjects.objects.create(
                    student_id=student_id,
                    class_subject_id=class_subject_id,
                    current_state_id=choice(all_state_ids)
                )
            created_cnt = created_cnt + 1 if not is_existed else created_cnt
        print(f"{created_cnt} успешно в сумме добавлено студентов к предметам")

    def handle(self, *args: Tuple[Any], **options: Dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # Data generation
        self.generate_classes()
        self.generate_general_subjects()
        self.generate_student_subj_states()
        self.generate_class_subjects()
        self.generate_topics(required_number=100)
        self.generate_trackways()
        self.generate_students()
        self.generate_student_registered_subjects(required_number=100)

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
