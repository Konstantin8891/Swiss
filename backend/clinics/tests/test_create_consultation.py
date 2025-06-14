"""Тест создания консультации."""

from typing import Dict

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 8,
                "clinic": 1,
            },
            {"status": status.HTTP_401_UNAUTHORIZED},
        ),
    ],
)
def test_create_consultation_guest_client(guest_client: APIClient, payload_data: Dict, expected_answer: Dict) -> None:
    """
    Тест создания консультации под гостевым клиентом.

    :param guest_client: клиент
    :param payload_data: body
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = guest_client.post(
        "/api/v1/clinics/consultations/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 8,
                "clinic": 1,
            },
            {"status": status.HTTP_403_FORBIDDEN},
        ),
    ],
)
def test_create_consultation_doctor_client(
    doctor_1_client: APIClient, payload_data: Dict, expected_answer: Dict
) -> None:
    """
    Тест создания консультации под врачом.

    :param doctor_1_client: клиент
    :param payload_data: body
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = doctor_1_client.post(
        "/api/v1/clinics/consultations/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 2,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 4,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "clinic": 1,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 4,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "start_date": "2300-06-13 07:00:48.252253+00:00",
                "end_date": "2300-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_201_CREATED},
        ),
    ],
)
def test_create_consultation_patient_client(
    patient_1_client: APIClient, payload_data: Dict, expected_answer: Dict
) -> None:
    """
    Тест создания консультации под врачом.

    :param patient_1_client: клиент
    :param payload_data: body
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = patient_1_client.post(
        "/api/v1/clinics/consultations/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")
