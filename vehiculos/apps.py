from django.apps import AppConfig


class VehiculosConfig(AppConfig):
    """
    Configuración de la aplicación Vehiculos.

    Responsabilidad:
    - Gestión de vehículos corporativos
    - Asociación vehículo ↔ usuario
    - Métricas y control administrativo

    Este módulo puede inicializar señales o lógica de arranque
    en el método ready().
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "vehiculos"
    verbose_name = "Gestión de Vehículos"

    def ready(self):
        """
        Punto de entrada para inicializar lógica de la app.

        Ejemplos de uso futuro:
        - Registro de signals
        - Inicialización de validadores
        - Auditoría
        """
        pass
