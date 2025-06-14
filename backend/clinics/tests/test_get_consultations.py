"""Тест получения консультаций."""

from typing import Dict

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "expected_answer",
    [
        ({"status": status.HTTP_401_UNAUTHORIZED}),
    ],
)
def test_get_consultations_guest_client(guest_client: APIClient, expected_answer: Dict) -> None:
    """
    Тест получения консультаций под гостевым клиентом.

    :param guest_client: клиент
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = guest_client.get("/api/v1/clinics/consultations/")
    assert response.status_code == expected_answer.get("status")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Матвей"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "Семочкин"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "Михайлович"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "dddddddddd"},
            {"status": status.HTTP_200_OK, "len_data": 0},
        ),
    ],
)
def test_get_consultations_patient_client(patient_2_client: APIClient, query_data: Dict, expected_answer: Dict) -> None:
    """
    Тест получения консультаций под пациентом.

    :param patient_2_client: клиент
    :param query_data: квери параметры
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = patient_2_client.get(
        "/api/v1/clinics/consultations/",
        data=query_data,
    )
    assert response.status_code == expected_answer.get("status")
    assert len(response.json().get("results")) == expected_answer.get("len_data")
    assert "count" in response.json().keys()
    assert "next" in response.json().keys()
    assert "previous" in response.json().keys()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {},
            {"status": status.HTTP_200_OK, "len_data": 3},
        ),
        (
            {"search": "Иван"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Михайлов"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Петрович"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Семен"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "Феоктистов"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "Александрович"},
            {"status": status.HTTP_200_OK, "len_data": 1},
        ),
        (
            {"search": "dddddddddd"},
            {"status": status.HTTP_200_OK, "len_data": 0},
        ),
    ],
)
def test_get_consultations_doctor_client(doctor_1_client: APIClient, query_data: Dict, expected_answer: Dict) -> None:
    """
    Тест получения консультаций.

    :param doctor_1_client: клиент
    :param query_data: квери параметры
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = doctor_1_client.get(
        "/api/v1/clinics/consultations/",
        data=query_data,
    )
    assert response.status_code == expected_answer.get("status")
    assert len(response.json().get("results")) == expected_answer.get("len_data")
    assert "count" in response.json().keys()
    assert "next" in response.json().keys()
    assert "previous" in response.json().keys()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {},
            {"status": status.HTTP_200_OK, "len_data": 4},
        ),
        (
            {"search": "Иван"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Михайлов"},
            {"status": status.HTTP_200_OK, "len_data": 3},
        ),
        (
            {"search": "Петрович"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Семен"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Феоктистов"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "Александрович"},
            {"status": status.HTTP_200_OK, "len_data": 2},
        ),
        (
            {"search": "dddddddddd"},
            {"status": status.HTTP_200_OK, "len_data": 0},
        ),
    ],
)
def test_get_consultations_admin_client(admin_1_client: APIClient, query_data: Dict, expected_answer: Dict) -> None:
    """
    Тест получения консультаций под админом.

    :param admin_1_client: клиент
    :param query_data: квери параметры
    :param expected_answer: ожидаемый ответ
    :return: None
    """
    response = admin_1_client.get(
        "/api/v1/clinics/consultations/",
        data=query_data,
    )
    assert response.status_code == expected_answer.get("status")
    assert len(response.json().get("results")) == expected_answer.get("len_data")
    assert "count" in response.json().keys()
    assert "next" in response.json().keys()
    assert "previous" in response.json().keys()
