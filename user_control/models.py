from django.db import models
from control.models import Company, Branch

# User Model
class Users(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
