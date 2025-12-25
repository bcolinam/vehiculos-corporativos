"""
Configuración de rutas internas para la aplicación Core.
Maneja la lógica de visualización de las páginas estáticas y principales.
"""

from django.urls import path
from .views import HomeView, AboutView

# El namespace es obligatorio para que {% url 'core:about' %} funcione
app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
]