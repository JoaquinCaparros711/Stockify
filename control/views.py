from django.shortcuts import render
from rest_framework import viewsets
from .serializer import *
from .models import *


# Create your views here.
class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class BranchView(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
class BranchStockView(viewsets.ModelViewSet):
    serializer_class = BranchStockSerializer
    queryset = BranchStock.objects.all()
    
class StockMovementView(viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    queryset = StockMovement.objects.all()