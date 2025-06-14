"""Базовые миксины."""

from django.db import models
from django.utils.translation import gettext as _


class DateMixin(models.Model):
    """Миксин создания/обновления для моделей."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updates_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        """Мета класс модели."""

        abstract = True
