"""Админка clinics."""

from clinics.models import Clinic, Specialization
from django.contrib import admin


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    """Админ-класс специализаций."""

    pass


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    """Админ-класс клиник."""

    pass
