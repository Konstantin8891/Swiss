"""Пагинация."""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class ConsultationPagination(PageNumberPagination):
    """Пагинация консультации."""

    page_size = settings.CONSULTATION_PAGE_SIZE
