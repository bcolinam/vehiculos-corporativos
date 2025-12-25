from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied

from .models import Vehiculo
from .forms import VehiculoForm

# --- Helpers de Seguridad ---

def admin_required(user):
    """Verifica si el usuario es staff. Si no lo es, lanza PermissionDenied o redirige."""
    if not user.is_staff:
        return False
    return True

# --- Vistas del Sistema ---

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Dashboard principal.
    - Admin: Ve métricas de toda la flota y estadísticas por usuario.
    - Usuario: Solo ve el estado de sus vehículos asignados.
    """
    user = request.user
    
    # Optimizamos con select_related para evitar el problema de N+1 queries al acceder a 'usuario'
    if user.is_staff:
        vehiculos_qs = Vehiculo.objects.select_related("usuario").all()
    else:
        # El usuario normal solo ve lo suyo
        vehiculos_qs = Vehiculo.objects.filter(usuario=user)

    # Estadísticas para el Administrador
    stats_usuarios = []
    if user.is_staff:
        stats_usuarios = list(
            Vehiculo.objects.values("usuario__username")
            .annotate(total=Count("id"))
            .order_by("-total")[:5] # Top 5 usuarios con más vehículos
        )

    context = {
        "metricas": {
            "total": vehiculos_qs.count(),
            "activos": vehiculos_qs.filter(activo=True).count(),
            "inactivos": vehiculos_qs.filter(activo=False).count(),
            "stats_usuarios": stats_usuarios,
        },
        "es_admin": user.is_staff,
        # Mostramos los últimos 5 registros según el nivel de acceso
        "ultimos_vehiculos": vehiculos_qs.order_by("-fecha_creacion")[:5]
    }

    return render(request, "vehiculos/dashboard.html", context)

@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def registrar_vehiculo(request: HttpRequest) -> HttpResponse:
    """Solo el staff puede registrar nuevos vehículos."""
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, f"Éxito: {vehiculo.patente} registrado correctamente.")
            return redirect("vehiculos:dashboard")
    else:
        form = VehiculoForm()

    return render(request, "vehiculos/registro.html", {"form": form})

@login_required
def detalle_vehiculos(request: HttpRequest) -> HttpResponse:
    """
    Lista completa de vehículos.
    Filtra automáticamente si el usuario no es administrador.
    """
    if request.user.is_staff:
        vehiculos = Vehiculo.objects.select_related("usuario").all().order_by("-fecha_creacion")
    else:
        vehiculos = Vehiculo.objects.filter(usuario=request.user).order_by("patente")

    return render(request, "vehiculos/detalle.html", {
        "vehiculos": vehiculos,
        "es_admin": request.user.is_staff,
    })

@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def editar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    """Edición restringida a Staff."""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehículo {vehiculo.patente} actualizado.")
            return redirect("vehiculos:detalle_vehiculos") # Nombre de URL corregido
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/editar.html", {
        "form": form,
        "vehiculo": vehiculo,
    })

@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def eliminar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    """Eliminación física del registro. Solo Staff."""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        patente = vehiculo.patente
        vehiculo.delete()
        messages.warning(request, f"El vehículo {patente} ha sido eliminado del sistema.")
        return redirect("vehiculos:detalle_vehiculos")

    return render(request, "vehiculos/eliminar.html", {"vehiculo": vehiculo})