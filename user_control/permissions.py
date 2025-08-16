from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Permiso personalizado: permite acceso de solo lectura (GET) a cualquier usuario autenticado,
    y acceso completo (POST, PUT, DELETE) solo a los usuarios administradores.
    """
    def has_permission(self, request, view):
        # Primero, nos aseguramos de que el usuario esté logueado.
        if not request.user or not request.user.is_authenticated:
            return False

        # Si el método de la petición es seguro (GET, HEAD, OPTIONS),
        # permitimos el acceso a todos los usuarios logueados.
        if request.method in SAFE_METHODS:
            return True

        # Si el método no es seguro (POST, PUT, DELETE),
        # solo permitimos el acceso si el rol del usuario es 'admin'.
        return request.user.role == 'admin'

class IsAdminUserCustom(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'