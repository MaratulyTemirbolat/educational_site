from django.contrib.admin import (
    register,
    ModelAdmin,
)

from teaching.models import (
    Teacher,
    TeacherSubjectClass,
)


@register(Teacher)
class TeacherAdmin(ModelAdmin):
    pass


@register(TeacherSubjectClass)
class TeacherSubjectClassModel(ModelAdmin):
    pass
