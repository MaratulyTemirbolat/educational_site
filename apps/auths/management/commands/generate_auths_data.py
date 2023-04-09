import names
from datetime import datetime
from random import choice
from typing import (
    Any,
    Tuple,
    Optional,
    Dict,
)

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from auths.models import CustomUser
from shops.models import Shop


class Command(BaseCommand):
    """Custom command for filling up database."""

    __email_patterns: Tuple[str] = (
        "mail.ru", "gmail.com", "outlook.com", "yahoo.com",
        "inbox.ru", "yandex.kz", "yandex.ru", "mail.kz",
    )
    __worker_states: tuple[bool] = (True, False,)

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def __generate_users(self, required_number: int = 0) -> None:
        def get_email(first_name: str, last_name: str) -> str:
            email_pattern: str = choice(self.__email_patterns)
            return f"{first_name.lower()}_{last_name.lower()}@{email_pattern}"

        def get_name() -> str:
            return names.get_first_name()

        def get_surname() -> str:
            return names.get_last_name()

        def generate_password() -> str:
            PASSWORD_PATTERN = "12345"
            return make_password(PASSWORD_PATTERN)

        def isWorker() -> bool:
            return choice(self.__worker_states)

        existed_shops_id: QuerySet[int] = Shop.objects.all().values_list(
            "id",
            flat=True
        )

        i: int
        for i in range(required_number):
            shop_id: Optional[int] = None
            if isWorker():
                shop_id = choice(existed_shops_id)

            first_name: str = get_name()
            last_name: str = get_surname()
            email: str = get_email(
                first_name=first_name,
                last_name=last_name
            )
            CustomUser.objects.get_or_create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                shop_id=shop_id,
                password=generate_password()
            )
        print(f"{required_number} пользователей успешно созданы")

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
