"""Пермишены пользователей."""

from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """Является ли пациентом."""

    def has_permission(self, request, view):
        """
        Has permission.

        :param request: Request
        :param view: View
        :return: Является ли пациентом boolean
        """
        if request.user.is_anonymous:
            return False
        if request.user.groups.first().id == 3:
            return True
        return False


class IsPatientOrAdmin(BasePermission):
    """Является ли админом или пациентом."""

    def has_permission(self, request, view):
        """
        Has permission.

        :param request: Request
        :param view: View
        :return: Является ли админом/пациентом boolean
        """
        if request.user.is_anonymous:
            return False
        if request.user.groups.first().id in (2, 3):
            return True
        return False


class IsAdmin(BasePermission):
    """Является ли админом."""

    def has_permission(self, request, view) -> bool:
        """
        Has permission.

        :param request: запрос
        :param view: вью
        :return: Имеет разрешение/не имеет boolean
        """
        if request.user.is_anonymous:
            return False
        if request.user.groups.first().id == 2:
            return True
        return False
