"""Фильтры приложения clinics."""

from typing import Any

from clinics.models import Consultation
from django.db.models import QuerySet
from django_filters import CharFilter, FilterSet


class ConsultationFilter(FilterSet):
    """Фильтр консультаций."""

    status = CharFilter(method="filter_status")

    class Meta:
        """Мета класс фильтра."""

        model = Consultation
        fields = ("status",)

    def filter_status(self, queryset: QuerySet, name: Any, value: str) -> QuerySet:
        """
        Метод фильтрации по статусу.

        :param queryset: кверисет
        :param name: не используется
        :param value: значение
        :return: кверисет
        """
        return queryset.filter(status=value)
