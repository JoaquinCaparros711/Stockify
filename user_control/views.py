from django.shortcuts import render
from rest_framework import viewsets
from user_control.models import Users
from .serializer import UserSerializer
    
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    
