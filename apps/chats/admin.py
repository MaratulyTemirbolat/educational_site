from django.contrib.admin import (
    register,
    ModelAdmin,
)

from abstracts.admin import AbstractAdminIsDeleted
from chats.models import (
    Message,
    PersonalChat,
)


@register(Message)
class MessageAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(PersonalChat)
class PersonalChatAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...
