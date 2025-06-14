"""Сервисы auth."""

from typing import Dict

from django.contrib.auth.models import Group
from users.models import User


def register_user(data: Dict) -> User:
    """
    Регистрация пользователя.

    :param data: валидированный словарь пользовталя
    :return: модель пользователя
    """
    password = data["password"]
    del data["password"]
    specializations = data.get("specializations")
    if "specializations" in data.keys():
        del data["specializations"]
    print("data")
    print(data)
    user = User.objects.create(**data)
    user.set_password(password)
    user.save()
    if specializations:
        group = Group.objects.get(id=1)
        user.groups.add(group)
        user.specializations.set(specializations)
    else:
        group = Group.objects.get(id=3)
        user.groups.add(group)
    return user
