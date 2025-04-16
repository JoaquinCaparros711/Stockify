# 📦 Proyecto Programación – Stockify

## 📄 Descripción del Proyecto
**Nombre**: Stockify

**Descripción**:  
Stockify es una aplicación web para la gestión de stock destinada a pequeñas y medianas empresas (PyMEs) que deseen administrar el inventario de sus productos de manera centralizada, permitiendo gestionar múltiples sucursales bajo una misma cuenta de empresa.

Cada empresa podrá registrar sus sucursales, crear sus usuarios para cada sucursal, cargar productos, controlar stock, ver reportes y realizar movimientos de ingreso o egreso de mercadería.

El sistema contará con:

- Autenticación de usuarios.
- Control de usuarios por empresa.
- Gestión de sucursales.
- Gestión de productos.
- Gestión de movimientos de stock.

---

## 👥 Usuarios del Sistema

### 1. Administrador de Empresa
- Registra la empresa en la plataforma.
- Crea y gestiona las sucursales.
- Crea usuarios para su empresa.
- Gestiona productos y stock de todas las sucursales.
- Visualiza reportes generales.

### 2. Empleado de Sucursal
- Administra el stock solo de la sucursal a la que pertenece.
- Registra movimientos de ingreso y egreso de stock.
- Visualiza reportes solo de su sucursal.

---

## ✅ Requisitos Funcionales

- Registro y login de usuarios.
- Alta de nuevas empresas.
- Alta, baja y modificación de sucursales por empresa.
- Alta, baja y modificación de productos por empresa.
- Ingreso y egreso de stock en sucursales.
- Visualización del stock actual por sucursal y total de la empresa.
- Reportes de movimientos (filtrables por fechas y sucursal).
- Gestión de usuarios internos (Administrador crea empleados).
- Validación de stock negativo (no permitir egresos si no hay stock).
- Acceso restringido según tipo de usuario.

---

## 🚀 Tecnologías utilizadas

- **Backend**: Django
- **Frontend**: React.js
- **Base de Datos**: MySQL
- **Autenticación**: Django Authentication
- **API**: Django REST Framework

---

## 🛠️ Requisitos

- Python 3.10+
- Node.js 18+
- MySQL 8.x
- pipenv o venv
- npm o yarn

---

## ⚙️ Configuración inicial

### 🔧 Backend
1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/stockify.git
cd backend
```

2. Crear entorno virtual e instalar dependencias:

```bash
python -m venv env
source env/bin/activate
```

3. Crear base de datos en MySQL:

```sql
CREATE DATABASE stockify_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Configurar `.env` con credenciales de base de datos.

5. Migrar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Ejecutar servidor:

```bash
python manage.py runserver
```
