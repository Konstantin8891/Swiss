"""Сервисы приложения clinics."""

from typing import Dict

from clinics.models import Consultation
from users.models import User


def create_consultation(data: Dict, user: User) -> Consultation:
    """
    Создание пользователя.

    :param data: валидированный словарь сериализатора
    :param user: объект User
    :return: объект Consultation
    """
    doctor = data["doctor"]
    del data["doctor"]
    clinic = data["clinic"]
    del data["clinic"]
    consultation = Consultation.objects.create(
        doctor=doctor, patient=user, clinic=clinic, status=Consultation.Status.waiting, **data
    )
    consultation.save()
    return consultation


def update_consultation(consultation: Consultation, data: Dict) -> Consultation:
    """
    Изменение консультации.

    :param consultation: объект Consultation
    :param data: валидированный словарь сериализатора
    :return: объект Consultation
    """
    consultation.start_date = data["start_date"]
    consultation.end_date = data["end_date"]
    consultation.clinic = data["clinic"]
    consultation.doctor = data["doctor"]
    consultation.save()
    return consultation


def patch_status(consultation: Consultation, data: Dict) -> Consultation:
    """
    Изменение статуса консультации.

    :param consultation: объект Consultation
    :param data: валидированный словарь сериализатора
    :return: объект Consultation
    """
    consultation.status = data["status"]
    consultation.save()
    return consultation
