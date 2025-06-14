"""Сериализаторы пользовталей."""

from clinics.models import Specialization
from rest_framework import serializers
from users.models import User


class SpecializationSerializer(serializers.ModelSerializer):
    """Сериализатор специализации."""

    class Meta:
        """Мета класс сериализатора."""

        model = Specialization
        fields = ("id", "name")


class DoctorSerializer(serializers.ModelSerializer):
    """Сериализатор врача."""

    specializations = SpecializationSerializer(many=True)

    class Meta:
        """Мета класс сериализатора."""

        model = User
        fields = ("id", "first_name", "last_name", "middle_name", "specializations")


class PatientSerializer(serializers.ModelSerializer):
    """Сериализатор пациента."""

    class Meta:
        """Мета класс сериализатора."""

        model = User
        fields = ("id", "first_name", "last_name", "middle_name", "phone", "email")
