from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .models import Vehiculo
from .forms import VehiculoForm


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Dashboard principal del módulo de vehículos.
    """

    # Query base optimizada
    vehiculos_qs = Vehiculo.objects.select_related("usuario")

    # SOLUCIÓN: Convertimos el QuerySet a una lista estándar de diccionarios
    # usando list(). Sin esto, json_script arroja el error TypeError.
    por_usuario_data = list(
        vehiculos_qs
        .values("usuario__username")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    metricas = {
        "total": vehiculos_qs.count(),
        "activos": vehiculos_qs.filter(activo=True).count(),
        "inactivos": vehiculos_qs.filter(activo=False).count(),
        "por_usuario": por_usuario_data,  # Ahora es una lista serializable
    }

    context = {
        "metricas": metricas,
    }

    return render(
        request,
        "vehiculos/dashboard.html",
        context,
    )

# --- El resto de tus vistas se mantienen iguales ---

@login_required
def registrar_vehiculo(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo registrado correctamente")
            return redirect("vehiculos:dashboard")
    else:
        form = VehiculoForm()
    return render(request, "vehiculos/registro.html", {"form": form})

@login_required
def detalle_vehiculos(request: HttpRequest) -> HttpResponse:
    vehiculos = Vehiculo.objects.select_related("usuario").order_by("patente")
    return render(request, "vehiculos/detalle.html", {"vehiculos": vehiculos})

@login_required
def editar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente")
            return redirect("vehiculos:detalle")
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculos/editar.html", {"form": form, "vehiculo": vehiculo})

@login_required
def eliminar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado correctamente")
        return redirect("vehiculos:detalle")
    return render(request, "vehiculos/eliminar.html", {"vehiculo": vehiculo})