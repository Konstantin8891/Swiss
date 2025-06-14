"""Тест изменения консультации."""

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
                "start_date": "2200-06-13 07:00:48.252253Z",
                "end_date": "2200-06-13 08:00:00Z",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_401_UNAUTHORIZED},
        ),
    ],
)
def test_put_consultation_guest_client(guest_client: APIClient, payload_data: Dict, expected_answer: Dict) -> None:
    """
    Тест изменния консультации под гостевым клиентом.

    :param guest_client: клиент
    :param payload_data: body
    :param expected_answer: ожэидаемый ответ
    :return: None
    """
    response = guest_client.put(
        "/api/v1/clinics/consultations/1/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 5,
                "clinic": 2,
            },
            {
                "status": status.HTTP_200_OK,
                "start_date": "2200-06-13T07:00:48.252253Z",
                "end_date": "2200-06-13T08:00:00Z",
                "doctor": 5,
                "clinic": 2,
            },
        ),
        (
            {
                "start_date": "2201-06-13 07:00:48.252253+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {"end_date": "2200-06-13 08:00:00+00:00", "doctor": 4, "clinic": 1},
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "clinic": 1,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 4,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00+00:00",
                "doctor": 4,
                "clinic": 2,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 5,
                "clinic": 1,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 2,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
    ],
)
def test_put_consultation_patient_1_client(
    patient_1_client: APIClient, payload_data: Dict, expected_answer: Dict
) -> None:
    """
    Тест изменения консультации под пациентом.

    :param patient_1_client: клиент
    :param payload_data: body
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = patient_1_client.put(
        "/api/v1/clinics/consultations/1/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")
    if response.status_code == 200:
        assert response.json()["start_date"] == expected_answer.get("start_date")
        assert response.json()["end_date"] == expected_answer.get("end_date")
        assert response.json()["doctor"]["id"] == expected_answer.get("doctor")
        assert response.json()["clinic"]["id"] == expected_answer.get("clinic")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {
                "status": status.HTTP_200_OK,
                "start_date": "2200-06-13T07:00:48.252253Z",
                "end_date": "2200-06-13T08:00:00Z",
                "doctor": 4,
                "clinic": 1,
            },
        ),
        (
            {
                "start_date": "2201-06-13 07:00:48.252253+00:00",
                "doctor": 4,
                "clinic": 1,
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {"end_date": "2200-06-13 08:00:00+00:00", "doctor": 4, "clinic": 1},
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "clinic": 1,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 4,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00+00:00",
                "doctor": 4,
                "clinic": 2,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 5,
                "clinic": 1,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
        (
            {
                "start_date": "2200-06-13 07:00:48.252253+00:00",
                "end_date": "2200-06-13 08:00:00+00:00",
                "doctor": 4,
                "clinic": 2,
            },
            {
                "status": status.HTTP_400_BAD_REQUEST,
            },
        ),
    ],
)
def test_put_consultation_admin_1_client(admin_1_client: APIClient, payload_data: Dict, expected_answer: Dict) -> None:
    """
    Тест изменения консультации под админом.

    :param admin_1_client: клиент
    :param payload_data: body
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = admin_1_client.put(
        "/api/v1/clinics/consultations/1/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")
    if response.status_code == 200:
        assert response.json()["start_date"] == expected_answer.get("start_date")
        assert response.json()["end_date"] == expected_answer.get("end_date")
        assert response.json()["doctor"]["id"] == expected_answer.get("doctor")
        assert response.json()["clinic"]["id"] == expected_answer.get("clinic")
