from django.db import models


# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    cuit = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Branch Model
class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# # User Model
# class User(models.Model):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('employee', 'Employee'),
#     ]
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     role = models.CharField(max_length=8, choices=ROLE_CHOICES)
#     branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.name


# Product Model
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# BranchStock Model
class BranchStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    current_stock = models.IntegerField(default=0)


# # StockMovement Model
# class StockMovement(models.Model):
#     MOVEMENT_TYPE_CHOICES = [
#         ('incoming', 'Incoming'),
#         ('outgoing', 'Outgoing'),
#     ]
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     movement_type = models.CharField(max_length=9, choices=MOVEMENT_TYPE_CHOICES)
#     quantity = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey('user_control.Users', on_delete=models.CASCADE)
#     description = models.TextField(null=True, blank=True)
#TODO crear nueva tabla history que no tenga ninguna clave foreigngkey

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    
    # --- Campos de Relación (los mantendremos por ahora para consistencia) ---
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('user_control.Users', on_delete=models.SET_NULL, null=True)

    # --- NUEVOS CAMPOS "CONGELADOS" ---
    # Guardamos una copia de los datos en el momento del movimiento
    product_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=150)
    price_at_movement = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto en el momento del movimiento")

    # --- Campos existentes ---
    movement_type = models.CharField(max_length=9, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)