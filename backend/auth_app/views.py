"""Вью приложения auth_app."""

from auth_app.serializers import (
    CustomTokenObtainPairSerializer,
    UserRegisterRequestSerializer,
    UserRegisterResponseSerializer,
)
from auth_app.services import register_user
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUserView(CreateAPIView):
    """Регистрация пользователя."""

    permission_classes = [AllowAny]
    serializer_class = UserRegisterRequestSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание пользователя.

        :param request: Request
        :param args:
        :param kwargs:
        :return: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_user(data=serializer.validated_data)
        return Response(UserRegisterResponseSerializer(instance=user).data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Вью для получения токенов."""

    serializer_class = CustomTokenObtainPairSerializer
