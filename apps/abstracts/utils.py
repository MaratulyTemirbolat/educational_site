from typing import (
    Optional,
    List,
)

from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Model

from abstracts.models import AbstractDateTime


def get_is_deleted(
    self,
    obj: Optional[Model] = None,
    obj_name: str = "Объект"
) -> str:
    """Get is deleted state of object."""
    if obj.datetime_deleted:
        return mark_safe(
            f'<p style="color:red; font-weight: bold; font-size: 17px;">\
                {obj_name} удалён</p>'
        )
    return mark_safe(
        f'<p style="color: green; font-weight: bold; font-size: 17px;">\
            {obj_name} не удалён</p>'
    )


def send_email(
    subject: str,
    text: str,
    receiver_emails: List[str]
) -> bool:
    """Send email."""
    try:
        send_mail(
            subject=subject,
            message=text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=receiver_emails
        )
        return True
    except Exception as e:
        print("Email error:", e)
        return False
