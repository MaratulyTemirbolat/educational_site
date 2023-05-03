from names import (
    get_first_name,
    get_last_name,
)
from datetime import datetime
from random import choice
from typing import (
    Any,
    Tuple,
    Dict,
)

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from auths.models import CustomUser


class Command(BaseCommand):
    """Custom command for filling up database."""

    __email_patterns: Tuple[str] = (
        "mail.ru", "gmail.com", "outlook.com", "yahoo.com",
        "inbox.ru", "yandex.kz", "yandex.ru", "mail.kz",
    )
    PASSWORD_PATTERN = "12345"

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def __generate_users(self, required_number: int = 0) -> None:
        def get_email(first_name: str, last_name: str) -> str:
            email_pattern: str = choice(self.__email_patterns)
            return f"{first_name.lower()}_{last_name.lower()}@{email_pattern}"

        def get_name() -> str:
            return get_first_name()

        def get_surname() -> str:
            return get_last_name()

        def generate_password() -> str:
            return make_password(self.PASSWORD_PATTERN)

        users_cnt: int = 0
        obj: CustomUser
        is_created: bool = False
        i: int
        for i in range(required_number):

            first_name: str = get_name()
            last_name: str = get_surname()
            email: str = get_email(
                first_name=first_name,
                last_name=last_name
            )
            obj, is_created = CustomUser.objects.get_or_create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password()
            )
            if is_created:
                users_cnt += 1
                print(f"Пользователь {obj} успешно создан")
        print(f"{users_cnt} пользователей успешно созданы")

    def handle(self, *args: Tuple[Any], **options: Dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # CustomUser data generation
        USERS_NUMBER = 50
        self.__generate_users(required_number=USERS_NUMBER)

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
