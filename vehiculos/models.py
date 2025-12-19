from django.db import models
from django.contrib.auth.models import User


class Vehiculo(models.Model):
    """
    Modelo que representa un vehículo corporativo.

    Cada vehículo:
    - Está asignado a un usuario responsable
    - Se identifica de forma única por su patente
    - Puede estar activo o inactivo
    - Mantiene información básica de auditoría
    """

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="vehiculos",
        verbose_name="Usuario responsable",
        help_text="Usuario responsable del vehículo",
    )

    patente = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        verbose_name="Patente",
        help_text="Patente única del vehículo",
    )

    marca = models.CharField(
        max_length=50,
        verbose_name="Marca",
        help_text="Marca del vehículo",
    )

    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo",
        help_text="Modelo del vehículo",
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el vehículo está activo",
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["patente"]
        indexes = [
            models.Index(fields=["patente"]),
            models.Index(fields=["usuario"]),
            models.Index(fields=["activo"]),
        ]

    def __str__(self) -> str:
        """
        Representación legible del vehículo.
        """
        return f"{self.patente} - {self.marca} {self.modelo}"
