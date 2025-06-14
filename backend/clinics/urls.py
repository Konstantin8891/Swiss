"""Маршрутизатор приложения клиник."""

from clinics.views import ConsultationListCreateView, ConsultationRetrieveUpdateDestroyView
from django.urls import include, path

clinics_urls = [
    path("consultations/", ConsultationListCreateView.as_view(), name="consultation_list_create"),
    path("consultations/<int:pk>/", ConsultationRetrieveUpdateDestroyView.as_view(), name="consultation_list_create"),
]

app_prefix = [
    path("clinics/", include(clinics_urls)),
]


urlpatterns = [
    path("v1/", include(app_prefix)),
]
