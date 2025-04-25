from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework import permissions, viewsets
from user_control.permissions import IsAdminUserCustom
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CompanyView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]
    serializer_class = CompanySerializer
    queryset = Company.objects.all() 

class BranchView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    
# class UserView(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
    
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def get_queryset(self):
        return Product.objects.filter(company=self.request.user.company)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class BranchStockView(viewsets.ModelViewSet):
    serializer_class = BranchStockSerializer
    permission_classes = [IsAuthenticated]
    queryset = BranchStock.objects.all()
    
class StockMovementView(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    queryset = StockMovement.objects.all()