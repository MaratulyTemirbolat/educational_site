from django.contrib.admin import (
    ModelAdmin,
    register,
)

from abstracts.admin import AbstractAdminIsDeleted
from subjectss.models import (
    Topic,
    Class,
    TrackWay,
    StudentSubjectState,
    GeneralSubject,
    ClassSubject,
    StudentRegisteredSubjects,
    Student,
)


@register(Topic)
class TopicAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Class)
class ClassAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(GeneralSubject)
class GeneralSubjectAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(StudentSubjectState)
class StudentSubjectStateAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(StudentRegisteredSubjects)
class StudentRegisteredSubjectsAdmin(ModelAdmin):
    ...


@register(ClassSubject)
class SubjectAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(TrackWay)
class TrackWayAdmin(AbstractAdminIsDeleted, ModelAdmin):
    ...


@register(Student)
class StudentAdmin(ModelAdmin):
    ...
