"""Тест получения консультации."""

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db()
def test_get_consultation_guest(guest_client: APIClient) -> None:
    """
    Тест получения консультации под гостевым клиентом.

    :param guest_client: клиент
    :return: None
    """
    response = guest_client.get("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db()
def test_get_consultation_patient_1_client_ok(patient_1_client: APIClient) -> None:
    """
    Тест полчуения консультации под пациентом: ок.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.get("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_get_consultation_patient_1_client_not_own(patient_1_client: APIClient) -> None:
    """
    Тест получения чужой консультации под пациентом.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.get("/api/v1/clinics/consultations/3/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_patient_1_client_not_found(patient_1_client: APIClient) -> None:
    """
    Тест получения несуществующей консультации под пациентом.

    :param patient_1_client: клиент
    :return: None
    """
    response = patient_1_client.get("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_patient_2_client_not_own(patient_2_client: APIClient) -> None:
    """
    Тест получения чужой консультации под пациентом.

    :param patient_2_client: клиент
    :return: None
    """
    response = patient_2_client.get("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_patient_2_client_ok(patient_2_client: APIClient) -> None:
    """
    Тест получения консультации под пациентом: ок.

    :param patient_2_client: клиент
    :return: None
    """
    response = patient_2_client.get("/api/v1/clinics/consultations/3/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_get_consultation_patient_2_client_not_found(patient_2_client: APIClient) -> None:
    """
    Тест получения несуществующей консультации под пациентом.

    :param patient_2_client: клиент
    :return: None
    """
    response = patient_2_client.get("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_doctor_1_client_ok(doctor_1_client: APIClient) -> None:
    """
    Тест получения консультации под врачом: ок.

    :param doctor_1_client:
    :return:
    """
    response = doctor_1_client.get("/api/v1/clinics/consultations/1/")
    assert response.status_code == 200


@pytest.mark.django_db()
def test_get_consultation_doctor_1_client_not_own(doctor_1_client: APIClient) -> None:
    """
    Тест получения чужой консультации под врачом.

    :param doctor_1_client: клиент
    :return: None
    """
    response = doctor_1_client.get("/api/v1/clinics/consultations/4/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_doctor_1_client_not_found(doctor_1_client: APIClient) -> None:
    """
    Тест получения несуществующей консультации под врачом.

    :param doctor_1_client: клиент
    :return: None
    """
    response = doctor_1_client.get("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_doctor_2_client_not_own(doctor_2_client: APIClient) -> None:
    """
    Тест получения чужой консультации под врачом.

    :param doctor_2_client: клиент
    :return: None
    """
    response = doctor_2_client.get("/api/v1/clinics/consultations/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_doctor_2_client_ok(doctor_2_client: APIClient) -> None:
    """
    Тест получения консультации под врачом: ок.

    :param doctor_2_client: клиент
    :return: None
    """
    response = doctor_2_client.get("/api/v1/clinics/consultations/4/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_get_consultation_doctor_2_client_not_found(doctor_2_client: APIClient) -> None:
    """
    Тест получения несуществующей консультации под врачом.

    :param doctor_2_client: клиент
    :return: None
    """
    response = doctor_2_client.get("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db()
def test_get_consultation_admin_1_client_ok(admin_1_client: APIClient) -> None:
    """
    Тест получения консультации под админом: ок.

    :param admin_1_client: клиент
    :return: None
    """
    response = admin_1_client.get("/api/v1/clinics/consultations/4/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_get_consultation_admin_1_client_not_found(admin_1_client: APIClient) -> None:
    """
    Тест получения несуществующей консультации под админом.

    :param admin_1_client: клиент
    :return: None
    """
    response = admin_1_client.get("/api/v1/clinics/consultations/300/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
