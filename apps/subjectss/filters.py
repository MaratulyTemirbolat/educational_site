from typing import Optional

from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.admin import ModelAdmin

from subjectss.models import Student


class PointsFilter(SimpleListFilter):
    """DeletedStateFilter."""

    title: str = "Количество баллов"
    parameter_name: str = "points"

    def lookups(
        self,
        request: WSGIRequest,
        model_admin: ModelAdmin
    ) -> list[tuple[str, str]]:
        """Return tuple of value and verbose value."""
        return [
            ("less_1000", "От 0 до 1000"),
            ("between_1000_2000", "От 1000 до 2000"),
            ("between_2000_3000", "От 2000 до 3000"),
            ("between_3000_4000", "От 3000 до 4000"),
            ("more_4000", "От 4000"),
        ]

    def queryset(
        self,
        request: WSGIRequest,
        queryset: QuerySet[Student]
    ) -> Optional[QuerySet[Student]]:
        """Return queryset by value."""
        if self.value() == "less_1000":
            return queryset.filter(points__lt=1000)
        if self.value() == "between_1000_2000":
            return queryset.filter(points__gte=1000, points__lt=2000)
        if self.value() == "between_2000_3000":
            return queryset.filter(points__gte=2000, points__lt=3000)
        if self.value() == "between_3000_4000":
            return queryset.filter(points__gte=3000, points__lt=4000)
        if self.value() == "more_4000":
            return queryset.filter(points__gte=4000)
