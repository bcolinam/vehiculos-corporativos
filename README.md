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
