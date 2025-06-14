"""Конфтест."""

import os
from datetime import timedelta
from typing import Callable, Generator

import pytest
from clinics.models import Clinic, Consultation, Specialization
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.utils import timezone
from pytest_django.plugin import DjangoDbBlocker
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture(scope="session")
def delete_db() -> None:
    """
    Удаление старой базы.

    :return: None
    """
    try:
        os.remove("db.sqlite3")
    except Exception:
        pass


@pytest.fixture(scope="session")
def django_db_setup(delete_db: Callable, django_db_blocker: DjangoDbBlocker) -> Generator:
    """
    Миграции.

    :param delete_db: фикстура
    :param django_db_blocker: DjangoDbBlocker
    :return: Генератор
    """
    with django_db_blocker.unblock():
        call_command("sqlflush")
    with django_db_blocker.unblock():
        call_command("migrate", "--noinput")
    yield


@pytest.fixture(autouse=True, scope="session")
def data(django_db_setup: Callable, django_db_blocker: DjangoDbBlocker) -> None:
    """
    Создание данных в тестовой базе данных.

    :param django_db_setup: фикстура
    :param django_db_blocker: DjangoDbBlocker
    :return: None
    """
    with django_db_blocker.unblock():
        doctor_group = Group.objects.get(id=1)
        admin_group = Group.objects.get(id=2)
        patient_group = Group.objects.get(id=3)
        admin = User.objects.create(
            id=1,
            first_name="Василий",
            last_name="Петров",
            middle_name="Иванович",
            username="admin_1",
            email="admin_1@example.com",
            phone="79111111111",
        )
        admin.set_password("Adminqwe1.")
        admin.save()
        admin.groups.add(admin_group)
        clinic_1 = Clinic.objects.create(
            id=1, legal_address="Юридический адрес", real_address="Фактический адрес", name="Клиника 1"
        )
        clinic_2 = Clinic.objects.create(
            id=2, legal_address="Юридический адрес", real_address="Фактический адрес", name="Клиника 2"
        )
        specialization_1 = Specialization.objects.create(id=1, name="Специализация 1")
        specialization_2 = Specialization.objects.create(id=2, name="Специализация 2")
        patient_1 = User.objects.create(
            id=2,
            first_name="Иван",
            last_name="Михайлов",
            middle_name="Петрович",
            username="patient_1",
            email="patient_1@example.com",
            phone="79111111112",
        )
        patient_1.set_password("Adminqwe1.")
        patient_1.save()
        patient_1.groups.add(patient_group)
        patient_2 = User.objects.create(
            id=3,
            first_name="Семен",
            last_name="Феоктистов",
            middle_name="Александрович",
            username="patient_2",
            email="patient_2@example.com",
            phone="79111111113",
        )
        patient_2.set_password("Adminqwe1.")
        patient_2.save()
        patient_2.groups.add(patient_group)
        doctor_1 = User.objects.create(
            id=4,
            first_name="Вениамин",
            last_name="Измайлов",
            middle_name="Харитонович",
            username="doctor_1",
            email="doctor_1@example.com",
            phone="79111111114",
        )
        doctor_1.set_password("Adminqwe1.")
        doctor_1.save()
        doctor_1.specializations.add(specialization_1)
        doctor_1.groups.add(doctor_group)
        doctor_1.clinics.add(clinic_1)
        doctor_2 = User.objects.create(
            id=5,
            first_name="Матвей",
            last_name="Семочкин",
            middle_name="Михайлович",
            username="doctor_2",
            email="doctor_2@example.com",
            phone="79111111115",
        )
        doctor_2.set_password("Adminqwe1.")
        doctor_2.save()
        doctor_2.specializations.add(specialization_2)
        doctor_2.groups.add(doctor_group)
        doctor_2.clinics.add(clinic_2)
        now = timezone.now()
        one_hour_after_now = now + timedelta(hours=1)
        Consultation.objects.create(
            id=1,
            start_date=now,
            end_date=one_hour_after_now,
            status=Consultation.Status.accepted,
            doctor=doctor_1,
            patient=patient_1,
            clinic=clinic_1,
        )
        Consultation.objects.create(
            id=2,
            start_date=now,
            end_date=one_hour_after_now,
            status=Consultation.Status.accepted,
            doctor=doctor_1,
            patient=patient_1,
            clinic=clinic_1,
        )
        Consultation.objects.create(
            id=3,
            start_date=now,
            end_date=one_hour_after_now,
            status=Consultation.Status.accepted,
            doctor=doctor_1,
            patient=patient_2,
            clinic=clinic_1,
        )
        Consultation.objects.create(
            id=4,
            start_date=now,
            end_date=one_hour_after_now,
            status=Consultation.Status.accepted,
            doctor=doctor_2,
            patient=patient_2,
            clinic=clinic_2,
        )


@pytest.fixture(autouse=True, scope="session")
def guest_client() -> APIClient:
    """
    Клиент.

    :return: клиент
    """
    return APIClient()


@pytest.fixture(autouse=True, scope="session")
def admin_1_client(
    guest_client: APIClient, django_db_blocker: DjangoDbBlocker, django_db_setup: Callable, data: Callable
) -> APIClient:
    """
    Клиент.

    :param guest_client: клиент
    :param django_db_blocker: DjangoDbBlocker
    :param django_db_setup: фикстура
    :param data: фикстура
    :return: клиент
    """
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post("/api/v1/auth_app/login/", data={"username": "admin_1", "password": "Adminqwe1."})
        token = str(response.json()["access"])
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client


@pytest.fixture(autouse=True, scope="session")
def patient_1_client(
    guest_client: APIClient, django_db_blocker: DjangoDbBlocker, django_db_setup: Callable, data: Callable
) -> APIClient:
    """
    Клиент.

    :param guest_client: клиент
    :param django_db_blocker: DjangoDbBlocker
    :param django_db_setup: фикстура
    :param data: фикстура
    :return: клиент
    """
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post(
            "/api/v1/auth_app/login/", data={"username": "patient_1", "password": "Adminqwe1."}
        )
        token = str(response.json().get("access"))
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client


@pytest.fixture(autouse=True, scope="session")
def patient_2_client(
    guest_client: APIClient, django_db_blocker: DjangoDbBlocker, django_db_setup: Callable, data: Callable
) -> APIClient:
    """
    Клиент.

    :param guest_client: клиент
    :param django_db_blocker: DjangoDbBlocker
    :param django_db_setup: фикстура
    :param data: фикстура
    :return: клиент
    """
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post(
            "/api/v1/auth_app/login/", data={"username": "patient_2", "password": "Adminqwe1."}
        )
        token = str(response.json().get("access"))
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client


@pytest.fixture(autouse=True, scope="session")
def doctor_1_client(
    guest_client: APIClient, django_db_blocker: DjangoDbBlocker, django_db_setup: Callable, data: Callable
) -> APIClient:
    """
    Клиент.

    :param guest_client: Клиент
    :param django_db_blocker: DjangoDbBlocker
    :param django_db_setup: фиксутра
    :param data: фикстура
    :return: клиент
    """
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post("/api/v1/auth_app/login/", data={"username": "doctor_1", "password": "Adminqwe1."})
        token = str(response.json().get("access"))
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client


@pytest.fixture(autouse=True, scope="session")
def doctor_2_client(
    guest_client: APIClient, django_db_blocker: DjangoDbBlocker, django_db_setup: Callable, data: Callable
) -> APIClient:
    """
    Клиент.

    :param guest_client: клиент
    :param django_db_blocker: DjangoDbBlocker
    :param django_db_setup: фикстура
    :param data: фикстура
    :return: клиент
    """
    with django_db_blocker.unblock():
        client = APIClient()
        response = guest_client.post("/api/v1/auth_app/login/", data={"username": "doctor_2", "password": "Adminqwe1."})
        token = str(response.json().get("access"))
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        return client
