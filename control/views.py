from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework import permissions, viewsets, mixins
from user_control.permissions import IsAdminUserCustom
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied



# Create your views here.
class CompanyView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.filter(id=self.request.user.company.id)



class BranchView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]
    serializer_class = BranchSerializer

    def get_queryset(self):
        return Branch.objects.filter(company=self.request.user.company)

    def perform_update(self, serializer):
        if serializer.instance.company != self.request.user.company:
            raise serializers.ValidationError("No tienes permiso para modificar esta sucursal.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.company != self.request.user.company:
            raise serializers.ValidationError("No tienes permiso para eliminar esta sucursal.")
        instance.delete()
    

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.role == 'employee':
            return Product.objects.filter(company=user.company)
        return Product.objects.none()

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
    
    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'admin' or instance.company != user.company:
            raise PermissionDenied("No tienes permiso para borrar este producto.")
        instance.delete()

    def perform_update(self, serializer):
        user = self.request.user
        if serializer.instance.company != user.company:
            raise PermissionDenied("No puedes modificar un producto que no es de tu empresa.")
        serializer.save()

    
class BranchStockView(viewsets.ModelViewSet):
    serializer_class = BranchStockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return BranchStock.objects.filter( branch__company=user.company )
        elif user.role == 'employee':
            return BranchStock.objects.filter( branch=user.branch )
        return BranchStock.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        branch = serializer.validated_data.get('branch')
        product = serializer.validated_data.get('product')

        if user.role == 'employee' and branch != user.branch:
            raise PermissionDenied("No puedes agregar productos a otra sucursal que no sea la tuya.")

        if branch.company != user.company:
            raise PermissionDenied("La sucursal no pertenece a tu empresa.")

        if product.company != user.company:
            raise PermissionDenied("No puedes agregar productos que no pertenezcan a tu empresa.")

        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role != 'admin' or instance.branch.company != user.company:
            raise PermissionDenied("No puedes modificar stock de otra empresa o si no sos admin.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role != 'admin' or instance.branch.company != user.company:
            raise PermissionDenied("No puedes borrar stock de otra empresa o si no sos admin.")
        return super().destroy(request, *args, **kwargs)

    
class StockMovementView(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # Admin: todos los movimientos de sucursales de su empresa
            return StockMovement.objects.filter(branch__company=user.company)
        elif user.role == 'employee':
            # Empleado: solo movimientos de su sucursal
            return StockMovement.objects.filter(branch=user.branch)
        return StockMovement.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        branch = serializer.validated_data.get('branch')
        product = serializer.validated_data.get('product')

        if user.role == 'employee' and branch != user.branch:
            raise PermissionDenied("No puedes agregar productos a otra sucursal que no sea la tuya.")

        if branch.company != user.company:
            raise PermissionDenied("La sucursal no pertenece a tu empresa.")

        if product.company != user.company:
            raise PermissionDenied("No puedes agregar productos que no pertenezcan a tu empresa.")

        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.branch.company != user.company:
            raise PermissionDenied("No puedes modificar stock de otra empresa.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role != 'admin' or instance.branch.company != user.company:
            raise PermissionDenied("No puedes borrar stock de otra empresa o si no sos admin.")
        return super().destroy(request, *args, **kwargs)
