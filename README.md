# 🚗 Sistema de Gestión de Vehículos Corporativos

## Descripción
Sistema web desarrollado en **Django** para la administración centralizada de vehículos corporativos, permitiendo registrar, asignar, modificar y visualizar vehículos asociados a usuarios del sistema.

El proyecto está orientado a entornos corporativos donde se requiere control, trazabilidad y visualización clara de activos vehiculares.

---

## Objetivo
Proveer una plataforma simple, segura y extensible para:
- Controlar el parque vehicular
- Asignar vehículos a usuarios
- Visualizar métricas y estados
- Facilitar la administración operativa

---

## Alcance Funcional

### Funcionalidades principales
- Autenticación de usuarios
- Registro de vehículos
- Asignación de vehículos a usuarios
- Edición y eliminación de registros
- Dashboard con métricas
- Gráficos de estado y asignación
- Vista detallada de todos los vehículos

### No incluido (por ahora)
- Control de roles avanzados
- Auditoría histórica
- Integraciones externas
- Exportación de datos

---

## Casos de Uso

### 1. Administrador
- Accede al dashboard
- Visualiza métricas generales
- Registra nuevos vehículos
- Edita o elimina vehículos
- Cambia la asignación de usuarios

### 2. Usuario autenticado
- Visualiza información de vehículos
- Accede a vistas autorizadas

---

## Tecnologías Utilizadas
- Python 3
- Django
- SQLite3
- HTML5 / CSS3
- Chart.js
- Git / GitHub

---

## Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/bcolinam/vehiculos-corporativos.git
cd vehiculos-corporativos
``` 
### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
``` 
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Ejecutar migraciones
```bash
python manage.py migrate
```
### 5. Crear superusuario
```bash
python manage.py createsuperuser
```
### 6. Ejecutar servidor
```bash
python manage.py runserver
```
##Uso del Sistema

Acceder a: http://127.0.0.1:8000

Login con usuario registrado

Acceso al dashboard principal

Gestión completa desde la interfaz web


## Estructura del Proyecto
vehiculos-corporativos/
├── core/               # Configuración principal Django
├── vehiculos/          # App de gestión vehicular
│   ├── templates/      # Templates HTML
│   ├── migrations/     # Migraciones de BD
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Lógica de vistas
│   ├── urls.py         # Rutas de la app
│   └── forms.py        # Formularios
├── manage.py
├── db.sqlite3
├── README.md
└── .gitignore

##Seguridad

Autenticación basada en Django Auth

Protección CSRF activa

Acceso restringido a vistas protegidas

Gestión centralizada de sesiones

###Próximos Pasos

Implementar roles y permisos

Auditoría de cambios

Exportación a Excel / CSV

Visualización avanzada de datos

Dockerización del proyecto

Despliegue productivo





