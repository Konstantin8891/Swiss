"""Маршрутизатор auth."""

from auth_app.views import CustomTokenObtainPairView, RegisterUserView
from django.urls import include, path

auth_app_urls = [
    path("registration/", RegisterUserView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]

app_prefix = [
    path("auth_app/", include(auth_app_urls)),
]


urlpatterns = [
    path("v1/", include(app_prefix)),
]
