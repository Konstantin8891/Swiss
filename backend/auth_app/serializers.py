"""Auth сериализаторы."""

from typing import Dict

from clinics.models import Specialization
from clinics.serializers import SpecializationSerializer
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from users.models import User


class UserRegisterRequestSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    specializations = serializers.PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(), many=True, required=False
    )

    class Meta:
        """Мета класс сериализатора."""

        model = User
        fields = ("username", "first_name", "last_name", "middle_name", "phone", "email", "password", "specializations")

    def validate(self, attrs: Dict) -> Dict:
        """
        Валидация.

        :param attrs: атрибуты сериализатора
        :return: атрибуты сериализатора
        """
        attrs["username"] = attrs["username"].lower()
        user = User.objects.filter(username=attrs["username"]).first()
        if user:
            raise ParseError("Имя пользователя занято")
        if attrs.get("email"):
            attrs["email"] = attrs["email"].lower()
            user = User.objects.filter(email=attrs["email"]).first()
            if user:
                raise ParseError("Почта привязана к другому пользователю")
        if not attrs["specializations"]:
            if not attrs.get("phone"):
                raise ParseError("Не указан номер телефона")
            user = User.objects.filter(username=attrs["phone"]).first()
            if user:
                raise ParseError("Телефон привязан к другому пользователю")
        return attrs


class UserRegisterResponseSerializer(serializers.ModelSerializer):
    """Сериализатор получения пользователя."""

    specializations = SpecializationSerializer(many=True)

    class Meta:
        """Мета класс сериализатора."""

        model = User
        fields = ("id", "username", "first_name", "last_name", "middle_name", "phone", "email", "specializations")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Переопределение сериализатора токенов."""

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        """
        Получение токена.

        :param user: пользователь
        :return: токены
        """
        token = super().get_token(user)
        group = user.groups.first()
        token["role"] = group.id
        return token
