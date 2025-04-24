from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework import permissions, viewsets
from user_control.permissions import IsAdminUserCustom


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
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
class BranchStockView(viewsets.ModelViewSet):
    serializer_class = BranchStockSerializer
    queryset = BranchStock.objects.all()
    
class StockMovementView(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    queryset = StockMovement.objects.all()