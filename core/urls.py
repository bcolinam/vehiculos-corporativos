from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# IMPORTANTE: En el archivo raíz NO se define app_name. 
# Los namespaces se definen dentro de cada archivo urls.py de cada aplicación.

urlpatterns = [
    # Administración de Django
    path("admin/", admin.site.urls),
    
    # Aplicaciones del Proyecto
    path("", include("core.views_urls")),          # Carga Home y About (Namespace: 'core')
    path("accounts/", include("accounts.urls")),    # Gestión de Usuarios (Namespace: 'accounts')
    path("vehiculos/", include("vehiculos.urls")),  # Gestión de Flota (Namespace: 'vehiculos')
    path("pages/", include("pages.urls")),          # Listados de Páginas (Namespace: 'pages')
    path("messages/", include("messaging.urls")),    # Mensajería (Namespace: 'messaging')
    
    # Plugins y Terceros
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

# Configuración para servir archivos multimedia en desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)