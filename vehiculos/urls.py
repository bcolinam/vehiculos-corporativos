from django.urls import path
from . import views

app_name = "vehiculos"

urlpatterns = [
    # Dashboard principal
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # Registro de vehículos
    path(
        "nuevo/",
        views.registrar_vehiculo,
        name="registrar_vehiculo",
    ),
# Módulo detalle
path("detalle/", views.detalle_vehiculos, name="detalle"),
path("editar/<int:pk>/", views.editar_vehiculo, name="editar"),
path("eliminar/<int:pk>/", views.eliminar_vehiculo, name="eliminar"),
]
