from rest_framework import permissions


class IsAdminUserCustom(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'