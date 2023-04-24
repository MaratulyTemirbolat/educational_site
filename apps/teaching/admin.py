from django.contrib.admin import (
    register,
    ModelAdmin,
)

from teaching.models import Teacher


@register(Teacher)
class TeacherAdmin(ModelAdmin):
    pass
