"""Тест изменения статусов консультации."""

from typing import Dict

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {"status": "finished"},
            {"status_code": status.HTTP_200_OK, "status": "finished"},
        ),
        (
            {"status": "fffffff"},
            {"status_code": status.HTTP_400_BAD_REQUEST},
        ),
    ],
)
def test_patch_consultation_admin_1_client(
    admin_1_client: APIClient, payload_data: Dict, expected_answer: Dict
) -> None:
    """
    Тест изменения статуса консультации под админом.

    :param admin_1_client: клиент
    :param payload_data: body
    :param expected_answer: словарь для сравнения с ответом сервера
    :return: None
    """
    response = admin_1_client.patch(
        "/api/v1/clinics/consultations/1/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status_code")
    if response.status_code == 200:
        assert response.json()["status"] == expected_answer.get("status")


@pytest.mark.django_db()
def test_patch_consultation_admin_1_client_not_found(admin_1_client: APIClient) -> None:
    """
    Тест изменения несуществующей консультации под админом.

    :param admin_1_client: клиент
    :return: None
    """
    response = admin_1_client.patch(
        "/api/v1/clinics/consultations/100/",
        data={"status": "finished"},
    )
    assert response.status_code == 404


@pytest.mark.django_db()
def test_patch_consultation_patient_1_client(patient_1_client: APIClient) -> None:
    """
    Тест измения статуса чужой консультации под пациентом.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.patch(
        "/api/v1/clinics/consultations/1/",
        data={"status": "finished"},
    )
    assert response.status_code == 403


@pytest.mark.django_db()
def test_patch_consultation_doctor_1_client(doctor_1_client: APIClient) -> None:
    """
    Тест изменения статуса консультации под врачом.

    :param doctor_1_client: клиент
    :return: None
    """
    response = doctor_1_client.put(
        "/api/v1/clinics/consultations/1/",
        data={"status": "finished"},
    )
    assert response.status_code == 403
