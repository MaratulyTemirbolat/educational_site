from datetime import datetime
from typing import (
    Optional,
    Any,
)
from random import (
    choice,
    sample,
    randint,
)

from django.core.management.base import BaseCommand
from django.db.models import QuerySet

from chats.models import (
    PersonalChat,
    Message,
)
from teaching.models import Teacher
from subjectss.models import Student


class Command(BaseCommand):
    """Custom command for filling up database."""
    __message_template_parts: tuple[str] = (
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

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def generate_chats(self, required_number: int = 0) -> None:
        """Generate test trackways in db."""
        all_student_ids: tuple[int] = tuple(
            Student.objects.values_list("id", flat=True)
        )
        all_teacher_ids: tuple[int] = tuple(
            Teacher.objects.values_list("id", flat=True)
        )
        created_cnt: int = 0
        is_created: bool = False
        _: PersonalChat

        i: int = 0
        for i in range(required_number):
            _, is_created = PersonalChat.objects.get_or_create(
                student_id=choice(all_student_ids),
                teacher_id=choice(all_teacher_ids)
            )
            created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} чатов успешно создано и добавлено")

    def generate_messages(self, messages_per_chat: int = 0) -> None:
        """Generate messages for all chats."""
        MIN_CONTENT_WORDS_NUM = 5
        MAX_CONTENT_WORDS_NUM = 30

        def get_random_content() -> str:
            ran_words_number: int = randint(
                MIN_CONTENT_WORDS_NUM,
                MAX_CONTENT_WORDS_NUM
            )
            return ' '.join(
                sample(
                    population=self.__message_template_parts,
                    k=ran_words_number
                )
            ).capitalize()

        all_chats: QuerySet[PersonalChat] = PersonalChat.objects.all()
        all_messages: list[Message] = []
        new_message: Optional[Message] = None
        created_messages: int = 0

        i: int
        chat: PersonalChat
        for chat in all_chats:
            for i in range(messages_per_chat):
                new_message = Message(
                    content=get_random_content(),
                    owner_id=choice([chat.student_id, chat.teacher_id]),
                    to_chat=chat
                )
                all_messages.append(new_message)
                created_messages += 1
        Message.objects.bulk_create(all_messages)
        print(f"{created_messages} сообщений в общем создано и добавлено")

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # Data generation
        self.generate_chats(50)
        self.generate_messages(50)

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
