from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_control.models import Users
from .serializer import UserSerializer, UserUpdateSerializer
from rest_framework import generics, permissions, viewsets, status, serializers
from user_control import serializer
from user_control.permissions import IsAdminUserCustom
from rest_framework_simplejwt.tokens import RefreshToken  # Para manejar tokens JWT
    



class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        # Permitir que usuarios no autenticados puedan acceder solo al método POST (crear usuario)
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """
        Elige un serializer diferente según la acción.
        """
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return super().get_serializer_class() # Usa el default para el resto

    def get_queryset(self):
        """
        Esta es la lógica corregida.
        Ahora, tanto el admin como el empleado recibirán la lista
        completa de usuarios de su empresa.
        """
        user = self.request.user
        if user.is_authenticated:
            # Devuelve todos los usuarios que pertenecen a la misma compañía.
            return Users.objects.filter(company=user.company)
        
        # Si no está autenticado, no devuelve nada.
        return Users.objects.none()

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"detail": "Ya estás autenticado. No puedes crear una nueva cuenta ni empresa."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        if user.role == 'admin':
            if instance.company != user.company:
                return Response({"detail": "No puedes modificar usuarios de otra empresa."}, status=status.HTTP_403_FORBIDDEN)
            return super().update(request, *args, **kwargs)

        # empleados no pueden actualizar
        return Response({"detail": "No tienes permiso para actualizar usuarios."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "No estás autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()

        if user.role == 'admin':
            if instance.company != user.company:
                return Response({"detail": "No puedes eliminar usuarios de otra empresa."}, status=status.HTTP_403_FORBIDDEN)
            return super().destroy(request, *args, **kwargs)

        # empleados no pueden borrar
        return Response({"detail": "No tienes permiso para eliminar usuarios."}, status=status.HTTP_403_FORBIDDEN)
    
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response({
#                 "message": "Login exitoso",
#                 "username": user.username,
#                 "role": user.role
#             }, status=status.HTTP_200_OK)
#         return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Si estás usando JWT, el logout invalida el refresh token
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Marca el token como inválido
            return Response({"message": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Token inválido o ya expirado"}, status=status.HTTP_400_BAD_REQUEST)

        # Código anterior basado en cookies (comentado):
        # if request.user.is_authenticated:
        #     logout(request)
        #     return Response({"message": "Sesión cerrada"}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"error": "No hay sesión activa"}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserByAdminView(generics.CreateAPIView):
    serializer_class = serializer.UserCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]  # ✅ Solo usuarios logueados

    def perform_create(self, serializer):
        # Validar que sea admin
        user = self.request.user
        if user.role != 'admin':
            raise serializers.ValidationError({"detail": "No tienes permiso para crear usuarios."})

        serializer.save()


class CreateBranchByAdminView(generics.CreateAPIView):
    serializer_class = serializer.BranchCreateByAdminSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'admin':
            raise serializers.ValidationError({"detail": "Solo los administradores pueden crear usuarios."})
        serializer.save()
        
def current_user(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "role": user.rol,
    })