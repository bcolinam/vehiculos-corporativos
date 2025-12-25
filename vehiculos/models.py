from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Vehiculo(models.Model):
    """
    Modelo que representa un vehículo corporativo.
    Optimizado para asignación flexible de usuarios y auditoría de flota.
    """

    # Al permitir null=True y blank=True, habilitamos que un vehículo 
    # se cree antes de tener un conductor asignado, o se reasigne después.
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # Si el usuario se elimina, el vehículo queda "libre" (NULL)
        null=True,
        blank=True,
        related_name="flota",
        verbose_name="Usuario responsable",
        help_text="Usuario asignado actualmente al vehículo.",
    )

    patente = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        verbose_name="Patente",
        help_text="Patente única (Formato: ABCD12 o AB1234).",
    )

    marca = models.CharField(
        max_length=50,
        verbose_name="Marca",
    )

    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo",
    )

    # Añadido: Año del vehículo (Crítico para seguros y logística)
    anio = models.PositiveIntegerField(
        verbose_name="Año",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year + 1)
        ],
        null=True,
        blank=True
    )

    # Añadido: Color (Útil para identificación visual rápida)
    color = models.CharField(
        max_length=30,
        verbose_name="Color",
        blank=True,
        null=True
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Estado Operativo",
        help_text="Indica si el vehículo está apto para circulación.",
    )

    # Auditoría automática
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última modificación",
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["-fecha_creacion"] # Los más nuevos aparecen primero
        indexes = [
            models.Index(fields=["patente"]),
            models.Index(fields=["activo"]),
        ]

    def __str__(self) -> str:
        return f"{self.patente} | {self.marca} {self.modelo} ({self.anio})"

    def save(self, *args, **kwargs):
        # Normalización: Siempre guardar la patente en mayúsculas
        self.patente = self.patente.upper().replace(" ", "").replace("-", "")
        super().save(*args, **kwargs)