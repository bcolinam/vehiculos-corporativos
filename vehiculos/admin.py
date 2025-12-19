from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Vehiculo.

    Objetivo:
    - Facilitar la gestión de vehículos corporativos
    - Permitir búsquedas rápidas
    - Evitar errores de edición
    """

    # Columnas visibles en el listado
    list_display = (
        "patente",
        "marca",
        "modelo",
        "usuario",
        "activo",
        "fecha_creacion",
    )

    # Campos por los que se puede buscar
    search_fields = (
        "patente",
        "marca",
        "modelo",
        "usuario__username",
    )

    # Filtros laterales
    list_filter = (
        "activo",
        "marca",
        "fecha_creacion",
    )

    # Orden por defecto
    ordering = ("-fecha_creacion",)

    # Campos de solo lectura (auditoría)
    readonly_fields = (
        "fecha_creacion",
    )

    # Organización del formulario en el admin
    fieldsets = (
        (
            "Información del Vehículo",
            {
                "fields": (
                    "patente",
                    "marca",
                    "modelo",
                    "activo",
                )
            },
        ),
        (
            "Asignación",
            {
                "fields": (
                    "usuario",
                )
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "fecha_creacion",
                )
            },
        ),
    )
