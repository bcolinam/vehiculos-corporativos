from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Page(models.Model):
    titulo = models.CharField(
        max_length=150,
        verbose_name="Título"
    )

    subtitulo = models.CharField(
        max_length=255,
        verbose_name="Subtítulo"
    )

    contenido = RichTextField(
        verbose_name="Contenido"
    )

    imagen = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True,
        verbose_name="Imagen"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pages",
        verbose_name="Autor"
    )

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "Página"
        verbose_name_plural = "Páginas"

    def __str__(self):
        return self.titulo
