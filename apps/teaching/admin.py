from django.contrib.admin import (
    register,
    ModelAdmin,
)

from teaching.models import (
    Teacher,
    TeacherSubjectClass,
)
from abstracts.admin import AbstractAdminIsDeleted


@register(Teacher)
class TeacherAdmin(AbstractAdminIsDeleted, ModelAdmin):
    pass


@register(TeacherSubjectClass)
class TeacherSubjectClassModel(ModelAdmin):
    pass
