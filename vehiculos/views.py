from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied

# NUEVO (import mínimo y seguro)
from openpyxl import Workbook

from .models import Vehiculo
from .forms import VehiculoForm


# --- Helpers de Seguridad ---

def admin_required(user):
    """Verifica si el usuario es staff."""
    return user.is_staff


# --- Vistas del Sistema ---

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Dashboard principal.
    - Admin: Ve métricas de toda la flota y estadísticas por usuario.
    - Usuario: Solo ve el estado de sus vehículos asignados.
    """
    user = request.user
    
    if user.is_staff:
        vehiculos_qs = Vehiculo.objects.select_related("usuario").all()
    else:
        vehiculos_qs = Vehiculo.objects.filter(usuario=user)

    stats_usuarios = []
    if user.is_staff:
        stats_usuarios = list(
            Vehiculo.objects.values("usuario__username")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

    context = {
        "metricas": {
            "total": vehiculos_qs.count(),
            "activos": vehiculos_qs.filter(activo=True).count(),
            "inactivos": vehiculos_qs.filter(activo=False).count(),
            "stats_usuarios": stats_usuarios,
        },
        "es_admin": user.is_staff,
        "ultimos_vehiculos": vehiculos_qs.order_by("-fecha_creacion")[:5]
    }

    return render(request, "vehiculos/dashboard.html", context)


@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def registrar_vehiculo(request: HttpRequest) -> HttpResponse:
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
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehículo {vehiculo.patente} actualizado.")
            return redirect("vehiculos:detalle_vehiculos")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/editar.html", {
        "form": form,
        "vehiculo": vehiculo,
    })


@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def eliminar_vehiculo(request: HttpRequest, pk: int) -> HttpResponse:
    vehiculo = get_object_or_404(Vehiculo, pk=pk)

    if request.method == "POST":
        patente = vehiculo.patente
        vehiculo.delete()
        messages.warning(request, f"El vehículo {patente} ha sido eliminado del sistema.")
        return redirect("vehiculos:detalle_vehiculos")

    return render(request, "vehiculos/eliminar.html", {"vehiculo": vehiculo})


# -------------------------------------------------------------------
# NUEVA VISTA — EXPORTACIÓN A EXCEL (NO rompe nada existente)
# -------------------------------------------------------------------

@login_required
@user_passes_test(admin_required, login_url='vehiculos:dashboard')
def exportar_vehiculos_excel(request: HttpRequest) -> HttpResponse:
    """
    Exporta SOLO los vehículos filtrados actualmente.
    Respeta filtros por GET y permisos.
    """

    # Base queryset
    qs = Vehiculo.objects.select_related("usuario")

    # 🔐 Seguridad por diseño (aunque solo staff accede)
    if not request.user.is_staff:
        qs = qs.filter(usuario=request.user)

    # 🔎 Filtros dinámicos desde la URL (?activo=1, ?usuario=juan, etc.)
    activo = request.GET.get("activo")
    usuario = request.GET.get("usuario")

    if activo is not None:
        qs = qs.filter(activo=activo.lower() in ["1", "true", "yes"])

    if usuario:
        qs = qs.filter(usuario__username__icontains=usuario)

    # 📊 Excel
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Vehículos"

    # Encabezados
    ws.append([
        "Patente",
        "Marca",
        "Modelo",
        "Responsable",
        "Estado"
    ])

    # Datos filtrados
    for v in qs:
        ws.append([
            v.patente,
            v.marca,
            v.modelo,
            v.usuario.get_full_name() or v.usuario.username,
            "Activo" if v.activo else "Inactivo"
        ])

    # Respuesta
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="vehiculos_filtrados.xlsx"'

    wb.save(response)
    return response

