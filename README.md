# 📦 Proyecto Programación – Stockify

## 📄 Descripción del Proyecto

**Nombre Tentativo:** Stockify

**Descripción:**  
*Stockify* es una aplicación web para la gestión de stock destinada a pequeñas y medianas empresas (PyMEs) que deseen administrar el inventario de sus productos de manera centralizada, permitiendo gestionar múltiples sucursales bajo una misma cuenta de empresa.

Cada empresa podrá registrar sus sucursales, cargar productos, controlar stock, ver reportes y realizar movimientos de ingreso o egreso de mercadería.

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

1. Registro y login de usuarios.
2. Alta de nuevas empresas.
3. Alta, baja y modificación de sucursales por empresa.
4. Alta, baja y modificación de productos por empresa.
5. Ingreso y egreso de stock en sucursales.
6. Visualización del stock actual por sucursal y total de la empresa.
7. Reportes de movimientos (filtrables por fechas y sucursal).
8. Gestión de usuarios internos (Administrador crea empleados).
9. Validación de stock negativo (no permitir egresos si no hay stock).
10. Acceso restringido según tipo de usuario.

---

💡 *Proyecto desarrollado con Django en el backend y React en el frontend.*
