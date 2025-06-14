"""Вью приложения клиники."""

from typing import Tuple

from clinics.filters import ConsultationFilter
from clinics.models import Consultation
from clinics.pagination import ConsultationPagination
from clinics.serializers import (
    ConsultationCreateUpdateSerializer,
    ConsultationStatusSerializer,
    ConsultationViewSerializer,
)
from clinics.services import create_consultation, patch_status, update_consultation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from users.permissions import IsAdmin, IsPatient, IsPatientOrAdmin


class ConsultationListCreateView(ListCreateAPIView):
    """Вью создания/получения списка консультаций."""

    pagination_class = ConsultationPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering_fields = ("created",)
    search_fields = (
        "doctor__first_name",
        "doctor__last_name",
        "doctor__middle_name",
        "patient__first_name",
        "patient__last_name",
        "patient__middle_name",
    )
    filterset_class = ConsultationFilter

    def get_queryset(self):
        """
        Кверисет.

        :return: кверисет
        """
        if self.request.user.groups.first().id == 1:
            return Consultation.objects.select_related("doctor", "patient", "clinic").filter(
                doctor_id=self.request.user.id
            )
        elif self.request.user.groups.first().id == 2:
            return Consultation.objects.select_related("doctor", "patient", "clinic").all()
        elif self.request.user.groups.first().id == 3:
            return Consultation.objects.select_related("doctor", "patient", "clinic").filter(
                patient_id=self.request.user.id
            )

    def get_serializer_class(self):
        """
        Сериализатор.

        :return: Сериализатор
        """
        if self.request.method == "POST":
            return ConsultationCreateUpdateSerializer
        elif self.request.method == "GET":
            return ConsultationViewSerializer

    def get_permissions(self) -> Tuple:
        """
        Пермишен.

        :return: Кортеж пермишенов
        """
        if self.request.method == "POST":
            return (IsPatient(),)
        elif self.request.method == "GET":
            print("self.request.user")
            print(self.request.user)
            return (IsAuthenticated(),)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание консультации.

        :param request: Request
        :param args:
        :param kwargs:
        :return: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consultation = create_consultation(data=serializer.validated_data, user=request.user)
        return Response(ConsultationViewSerializer(instance=consultation).data, status=status.HTTP_201_CREATED)


class ConsultationRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Вью удаления/получения/редактирования консультации."""

    def get_queryset(self):
        """
        Кверисет.

        :return: Кверисет
        """
        if self.request.user.groups.first().id == 1:
            return Consultation.objects.select_related("doctor", "patient", "clinic").filter(
                doctor_id=self.request.user.id
            )
        elif self.request.user.groups.first().id == 2:
            return Consultation.objects.select_related("doctor", "patient", "clinic").all()
        elif self.request.user.groups.first().id == 3:
            return Consultation.objects.select_related("doctor", "patient", "clinic").filter(
                patient_id=self.request.user.id
            )

    def get_serializer_class(self):
        """
        Сериализатор.

        :return: Сериализатор
        """
        if self.request.method == "PUT":
            return ConsultationCreateUpdateSerializer
        elif self.request.method == "GET":
            return ConsultationViewSerializer
        elif self.request.method == "PATCH":
            return ConsultationStatusSerializer

    def get_permissions(self) -> Tuple:
        """
        Пермишен.

        :return: Кортеж пермишенов
        """
        if self.request.method in ("PUT", "DELETE"):
            return (IsPatientOrAdmin(),)
        elif self.request.method == "GET":
            return (IsAuthenticated(),)
        elif self.request.method == "PATCH":
            return (IsAdmin(),)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение консультации.

        :param request: Request
        :param args:
        :param kwargs:
        :return: Response
        """
        consultation = self.get_object()
        serializer = self.get_serializer(consultation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.user.groups.first().id == 3 and consultation.patient != request.user:
            raise PermissionDenied("Доступ запрещён")
        consultation = update_consultation(consultation=consultation, data=serializer.validated_data)
        return Response(ConsultationViewSerializer(instance=consultation).data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs) -> Response:
        """
        Изменение статуса консультации.

        :param request: Request
        :param args:
        :param kwargs:
        :return: Response
        """
        consultation = self.get_object()
        serializer = self.get_serializer(consultation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        consultation = patch_status(consultation=consultation, data=serializer.validated_data)
        return Response(ConsultationViewSerializer(instance=consultation).data, status=status.HTTP_200_OK)
