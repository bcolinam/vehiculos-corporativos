"""
URL configuration for core project.

Responsabilidades:
- Exponer el panel de administración
- Gestionar autenticación (login / logout)
- Delegar URLs a las apps de dominio

Django 4.2.x
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ------------------------------------------------------------------
    # Administración Django
    # ------------------------------------------------------------------
    path("admin/", admin.site.urls),

    # ------------------------------------------------------------------
    # Autenticación (Django Auth)
    # ------------------------------------------------------------------
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # ------------------------------------------------------------------
    # Aplicación principal
    # ------------------------------------------------------------------
    path("", include("vehiculos.urls")),
]
