"""Конфиг приложения."""

from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Класс конфига."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_app"
