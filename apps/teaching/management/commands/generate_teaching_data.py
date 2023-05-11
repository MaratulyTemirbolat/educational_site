from datetime import datetime
from typing import Any
from random import (
    choice,
    choices,
    randint,
)

from django.core.management.base import BaseCommand

from subscriptions.models import (
    Status,
    Subscription,
)
from subjectss.models import ClassSubject
from auths.models import CustomUser
from teaching.models import Teacher


class Command(BaseCommand):
    """Custom command for filling up database."""
    TEACHER_STATE = (True, False,)

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Call parent constructor."""
        super().__init__(args, kwargs)

    def generate_teachers(self) -> None:
        """Generate test trackways in db."""
        all_user_ids: tuple[int] = tuple(
            CustomUser.objects.values_list("id", flat=True)
        )
        all_status_ids: tuple[int] = tuple(
            Status.objects.values_list("id", flat=True)
        )
        all_subscr_ids: tuple[int] = tuple(
            Subscription.objects.values_list("id", flat=True)
        )
        all_class_subjects: tuple[int] = tuple(
            ClassSubject.objects.all()
        )
        class_number: int = ClassSubject.objects.count()

        is_teacher: bool = False
        is_existed_teacher: bool = False
        add_subscr: bool = False
        created_cnt: int = 0
        teacher: Teacher

        user_id: int = 0
        for user_id in all_user_ids:
            is_teacher = choice(self.TEACHER_STATE)
            is_existed_teacher = Teacher.objects.filter(
                user_id=user_id
            ).exists()
            if is_teacher and not is_existed_teacher:
                add_subscr = choice((True, False,))
                teacher = Teacher.objects.create(
                    user_id=user_id,
                    subscription_id=choice(all_subscr_ids) if add_subscr else None,
                    status_subscription_id=choice(all_status_ids) if add_subscr else None
                )
                subjs: list[ClassSubject] = choices(
                    all_class_subjects,
                    k=randint(0, class_number)
                )
                subj: ClassSubject
                for subj in subjs:
                    teacher.tought_subjects.add(subj)
                created_cnt += 1
        print(f"{created_cnt} преподавателей успешно создано и добавлено")

    def handle(self, *args: tuple[Any], **options: dict[str, Any]) -> None:
        """Handle data filling."""
        start_time: datetime = datetime.now()

        # Data generation
        self.generate_teachers()

        print(
            "Генерация данных составила: {} секунд".format(
                (datetime.now()-start_time).total_seconds()
            )
        )
