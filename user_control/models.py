from django.db import models
from control.models import Company, Branch
from django.contrib.auth.models import AbstractUser
# Create your models here.
# User Model
class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name