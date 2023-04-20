from django.contrib.admin import register, ModelAdmin

from subscriptions.models import Subscription, Status
from abstracts.admin import AbstractAdminIsDeleted


@register(Subscription)
class SubscriptionAdmin(AbstractAdminIsDeleted, ModelAdmin):
    pass


@register(Status)
class StatusAdmin(AbstractAdminIsDeleted, ModelAdmin):
    pass
