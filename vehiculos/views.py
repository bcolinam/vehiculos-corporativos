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
    Dashboard principal del sistema de vehículos.

    - Admin/Superadmin: ven todos los vehículos y métricas globales
    - Usuario regular: solo ve sus vehículos asignados
    """

    user = request.user

    if user.is_staff:
        vehiculos_qs = Vehiculo.objects.select_related("usuario")
    else:
        vehiculos_qs = Vehiculo.objects.filter(usuario=user)

    por_usuario_data = []
    if user.is_staff:
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
        "por_usuario": por_usuario_data,
    }

    context = {
        "metricas": metricas,
        "es_admin": user.is_staff,
    }

    return render(request, "vehiculos/dashboard.html", context)


@login_required
def registrar_vehiculo(request: HttpRequest) -> HttpResponse:
    """
    Registro de vehículos.
    Solo administradores pueden acceder.
    """

    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para registrar vehículos")
        return redirect("vehiculos:dashboard")

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
    """
    Listado de vehículos.

    - Admin/Superadmin: ven todos
    - Usuario regular: solo los asignados
    """

    if request.user.is_staff:
        vehiculos = Vehiculo.objects.select_related("usuario").order_by("patente")
    else:
        vehiculos = Vehiculo.objects.filter(usuario=request.user).order_by("patente")

    context = {
        "vehiculos": vehiculos,
        "es_admin": request.user.is_staff,
    }

    return render(request, "vehiculos/detalle.html", context)


@login_required
def editar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Edición de vehículo.
    Solo administradores.
    """

    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para editar vehículos")
        return redirect("vehiculos:dashboard")

    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente")
            return redirect("vehiculos:detalle")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(
        request,
        "vehiculos/editar.html",
        {
            "form": form,
            "vehiculo": vehiculo,
        },
    )


@login_required
def eliminar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Eliminación de vehículo.
    Solo administradores.
    """

    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para eliminar vehículos")
        return redirect("vehiculos:dashboard")

    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado correctamente")
        return redirect("vehiculos:detalle")

    return render(
        request,
        "vehiculos/eliminar.html",
        {
            "vehiculo": vehiculo,
        },
    )
