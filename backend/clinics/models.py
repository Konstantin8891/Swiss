"""Модели приложения clinics."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from backend.models import DateMixin


class Specialization(DateMixin):
    """Специализация."""

    name = models.CharField(max_length=50, verbose_name=_("Specialization"))

    def __str__(self) -> str:
        """
        Строковое представление объекта.

        :return: str
        """
        return self.name


class Clinic(DateMixin):
    """Клиника."""

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    legal_address = models.TextField(verbose_name=_("Legal address"))
    real_address = models.TextField(verbose_name=_("Real address"))

    def __str__(self) -> str:
        """
        Строковое представление объекта.

        :return: str
        """
        return self.name


class Consultation(DateMixin):
    """Консультация."""

    class Status(models.TextChoices):
        """Енам статусов."""

        accepted = "accepted", _("accepted")
        waiting = "waiting", _("waiting")
        started = "started", _("started")
        finished = "finished", _("finished")
        payed = "payed", _("payed")

    start_date = models.DateTimeField(verbose_name=_("Start date"))
    end_date = models.DateTimeField(verbose_name=_("End date"))
    status = models.CharField(max_length=20, choices=Status.choices, verbose_name=_("Status"))
    doctor = models.ForeignKey(
        get_user_model(), verbose_name=_("Doctor"), on_delete=models.CASCADE, related_name="doctors_consultations"
    )
    patient = models.ForeignKey(
        get_user_model(), verbose_name=_("Patient"), on_delete=models.CASCADE, related_name="patients_consultations"
    )
    clinic = models.ForeignKey(Clinic, verbose_name=_("Clinic"), on_delete=models.CASCADE, related_name="consultations")
