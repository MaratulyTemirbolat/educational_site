from django.contrib.admin import (
    register,
    ModelAdmin,
)

from abstracts.admin import AbstractAdminIsDeleted
from subjectss.models import (
    Topic,
    Class,
    Subject,
    TrackWay,
    SubjectClassTopic,
)


@register(Topic)
class TopicAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Class)
class ClassAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Subject)
class SubjectAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(TrackWay)
class TrackWayAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(SubjectClassTopic)
class SubjectClassTopicAdmin(ModelAdmin):
    ...
