"""Админка пользователей."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Юзер админ класс."""

    pass
