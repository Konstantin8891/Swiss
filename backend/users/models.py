"""Модель пользователя."""

from clinics.models import Clinic, Specialization
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Middle name"))
    phone = PhoneNumberField(null=True, blank=True, verbose_name=_("Phone"))
    specializations = models.ManyToManyField(
        Specialization, related_name="doctors", verbose_name=_("Specializations"), blank=True, null=True
    )
    clinics = models.ManyToManyField(Clinic, related_name="doctors", verbose_name=_("Clinics"), blank=True, null=True)
