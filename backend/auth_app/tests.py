"""Тесты auth."""

import pytest
from rest_framework import status


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        (
            {
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "phone": "+79111111117",
                "email": "mihail4@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail4",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "phone": "+79111111117",
                "email": "mihail4@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail4",
                "first_name": "Михаил",
                "middle_name": "Михайлович",
                "phone": "+79111111117",
                "email": "mihail4@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail4",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "phone": "+79111111117",
                "email": "mihail4@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_201_CREATED},
        ),
        (
            {
                "username": "Mihail2",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "email": "mihail2@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_201_CREATED},
        ),
        (
            {
                "username": "patient_1",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "email": "mihail2@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail3",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "email": "patient_1@example.com",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail3",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "email": "mihail3@example.com",
                "password": "Adminqwe1.",
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail3",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "phone": "+79111111117",
                "password": "Adminqwe1.",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_201_CREATED},
        ),
        (
            {
                "username": "Mihail3",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "phone": "+79111111117",
                "email": "mihail4@example.com",
                "specializations": [1, 2],
            },
            {"status": status.HTTP_400_BAD_REQUEST},
        ),
        (
            {
                "username": "Mihail1",
                "first_name": "Михаил",
                "last_name": "Михайлов",
                "middle_name": "Михайлович",
                "phone": "+79111111111",
                "email": "mihail1@example.com",
                "password": "Adminqwe1.",
            },
            {"status": status.HTTP_201_CREATED},
        ),
    ],
)
def test_register(guest_client, payload_data, expected_answer):
    """
    Тест регистрации.

    :param guest_client: Клиент
    :param payload_data: body
    :param expected_answer: словарь ответа для сравнения с полученным ответом сервера
    :return:
    """
    response = guest_client.post(
        "/api/v1/auth_app/registration/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "payload_data, expected_answer",
    [
        ({"username": "doctor_1", "password": "Михайлов"}, {"status": status.HTTP_401_UNAUTHORIZED}),
        ({"username": "doctor_10", "password": "Adminqwe1."}, {"status": status.HTTP_401_UNAUTHORIZED}),
        ({"password": "Михайлов"}, {"status": status.HTTP_400_BAD_REQUEST}),
        ({"username": "doctor_1"}, {"status": status.HTTP_400_BAD_REQUEST}),
    ],
)
def test_login(guest_client, payload_data, expected_answer):
    """
    Тест логина.

    :param guest_client: Клиент
    :param payload_data: body
    :param expected_answer: словарь для сравнения с ответом сервера
    :return:
    """
    response = guest_client.post(
        "/api/v1/auth_app/login/",
        data=payload_data,
    )
    assert response.status_code == expected_answer.get("status")
