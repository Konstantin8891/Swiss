"""Сериализаторы приложения clinics."""

from typing import Dict

import pytz
from clinics.models import Clinic, Consultation, Specialization
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from users.serializers import DoctorSerializer, PatientSerializer


class ClinicSerializer(serializers.ModelSerializer):
    """Клиника."""

    class Meta:
        """Мета класс сериализатора."""

        model = Clinic
        fields = ("id", "legal_address", "real_address")


class SpecializationSerializer(serializers.ModelSerializer):
    """Специализация."""

    class Meta:
        """Мета класс сериализатора."""

        model = Specialization
        fields = ("id", "name")


class ConsultationCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление консультации."""

    doctor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    clinic = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all())

    class Meta:
        """Мета класс сериализатора."""

        model = Consultation
        fields = ("start_date", "end_date", "doctor", "clinic")

    def validate(self, attrs: Dict) -> Dict:
        """
        Валидация данных.

        :param attrs: атрибуты сериализатора
        :return: атрибуты сериализатора
        """
        now = timezone.now()
        if not attrs.get("start_date"):
            raise ParseError("Не указана дата начала")
        if not attrs.get("end_date"):
            raise ParseError("Не указана дата конца")
        if not attrs.get("doctor"):
            raise ParseError("Не указан врач")
        if not attrs.get("clinic"):
            raise ParseError("Не указана клиника")
        if attrs["doctor"].groups.first().id != 1:
            raise ParseError("Ошибка выбора доктора")
        if attrs["clinic"] not in attrs["doctor"].clinics.all():
            raise ParseError("Доктор не работает в данной клинике")
        attrs["start_date"] = attrs["start_date"].replace(tzinfo=pytz.UTC)
        attrs["end_date"] = attrs["end_date"].replace(tzinfo=pytz.UTC)
        if attrs["start_date"] < now:
            raise ParseError("Дата начала консультации меньше текущей")
        if attrs["start_date"] > attrs["end_date"]:
            raise ParseError("Дата начала консультации больше даты конца консультации")
        return attrs


class ConsultationViewSerializer(serializers.ModelSerializer):
    """Просмотр объекта консультации."""

    doctor = DoctorSerializer()
    patient = PatientSerializer()
    clinic = ClinicSerializer()

    class Meta:
        """Мета класс сериализатора."""

        model = Consultation
        fields = ("id", "start_date", "end_date", "status", "doctor", "patient", "clinic")


class ConsultationStatusSerializer(serializers.ModelSerializer):
    """Сериализатор статуса консультаций."""

    class Meta:
        """Мета класс сериализатора."""

        model = Consultation
        fields = ("status",)
