"""Тест удаления консультации."""

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_delete_consultation_guest(guest_client: APIClient) -> None:
    """
    Тест удаления консультации под гостевым клиентом.

    :param guest_client: клиент
    :return: None
    """
    response = guest_client.delete("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db()
def test_delete_consultation_patient_1_client_ok(patient_1_client: APIClient) -> None:
    """
    Тест удаления консультации под пациентом: ок.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.delete("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_delete_consultation_patient_1_client_not_own(patient_1_client: APIClient) -> None:
    """
    Тест удаление чужой консультации под пациентом.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.delete("/api/v1/clinics/consultations/3/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_delete_consultation_patient_1_client_not_found(patient_1_client: APIClient) -> None:
    """
    Тест получения консультации под пациентом: консультация не найдена.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.delete("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_delete_consultation_admin_1_client_ok(admin_1_client: APIClient) -> None:
    """
    Тест удаления консультации под админом: ок.

    :param admin_1_client: клиент
    :return: None
    """
    response = admin_1_client.delete("/api/v1/clinics/consultations/2/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db()
def test_delete_consultation_admin_1_client_not_found(admin_1_client: APIClient) -> None:
    """
    Тест удаления консультации под админом: консультация не найдена.

    :param admin_1_client: Клиент
    :return: None
    """
    response = admin_1_client.delete("/api/v1/clinics/consultations/200/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
