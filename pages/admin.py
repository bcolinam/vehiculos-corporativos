from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "fecha_creacion")
    search_fields = ("titulo", "subtitulo", "contenido")
    list_filter = ("fecha_creacion",)
