from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserSerializer
from ..control.models import User
    
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
