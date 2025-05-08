from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from user_control.models import Users
from .serializer import UserSerializer
from rest_framework import generics, permissions, viewsets
from user_control import serializer
from user_control.permissions import IsAdminUserCustom

    
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return Users.objects.filter(company=user.company)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                "message": "Login exitoso",
                "username": user.username,
                "role": user.role
            }, status=status.HTTP_200_OK)
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)

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