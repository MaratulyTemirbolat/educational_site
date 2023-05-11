from datetime import datetime
from typing import Any

from django.core.management.base import BaseCommand

from subscriptions.models import (
    Status,
    Subscription,
)


class Command(BaseCommand):
    """Custom command for filling up database."""

    SUBSCRIPTIONS_DATA = {
        "3 месяца": 3,
        "6 месяцев": 6,
        "9 месяцев": 9,
        "12 месяцев": 12,
    }
    SUBSCR_STATUS_NAMES = ("Активен", "Не Активен",)

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def generate_subscriptions(self) -> None:
        """Generate test trackways in db."""
        def get_subsc_description(name) -> str:
            return f"{name}'s subscription description."

        created_cnt: int = 0
        is_created: bool = False
        _: Subscription

        subscr: str
        for subscr in self.SUBSCRIPTIONS_DATA:
            _, is_created = Subscription.objects.get_or_create(
                name=subscr,
                description=get_subsc_description(subscr),
                duration=self.SUBSCRIPTIONS_DATA.get(subscr, 3)
            )
            created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} подписок успешно создано и добавлено в базу")

    def generate_subscription_statuses(self) -> None:
        """Generate subscription statuses."""
        created_cnt: int = 0
        is_created: bool = False
        _: Status

        status_name: str
        for status_name in self.SUBSCR_STATUS_NAMES:
            _, is_created = Status.objects.get_or_create(name=status_name)
            created_cnt = created_cnt + 1 if is_created else created_cnt
        print(f"{created_cnt} статус(-ов) для подсписок успешно создано")

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # Data generation
        self.generate_subscriptions()
        self.generate_subscription_statuses()

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
