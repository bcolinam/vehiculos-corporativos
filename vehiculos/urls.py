from django.urls import path
from . import views

app_name = "vehiculos"

urlpatterns = [
    # --- Dashboard Principal ---
    # Es la vista central que ven todos al entrar a /vehiculos/
    path(
        "", 
        views.dashboard, 
        name="dashboard"
    ),
    
    # --- Gestión de Listados ---
    # Nombre actualizado a 'detalle_vehiculos' para coincidir con el redirect de las vistas
    path(
        "listado/", 
        views.detalle_vehiculos, 
        name="detalle_vehiculos"
    ),

    # --- Operaciones de Registro (Solo Staff) ---
    path(
        "nuevo/", 
        views.registrar_vehiculo, 
        name="registro"  # Nombre más corto y estándar
    ),
    
    # --- Operaciones de Modificación (Solo Staff) ---
    path(
        "editar/<int:pk>/", 
        views.editar_vehiculo, 
        name="editar"
    ),
    
    path(
        "eliminar/<int:pk>/", 
        views.eliminar_vehiculo, 
        name="eliminar"
    ),
]