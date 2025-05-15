from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_control.models import Users
from control.models import Company, Branch, Product, BranchStock, StockMovement


class StockMovementTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Empresa Test",
            cuit="12345678901",
            email="empresa@test.com",
            phone="1234567890",
            address="Calle Falsa 123"
        )

        self.branch = Branch.objects.create(
            company=self.company,
            name="Sucursal A",
            address="Av. Siempre Viva",
            phone="111111111"
        )

        self.product = Product.objects.create(
            company=self.company,
            name="Producto X",
            description="Desc",
            category="Cat",
            price=10.0
        )

        self.admin = Users.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="Admin123!",
            name="Admin",
            company=self.company,
            role="admin"
        )

        self.employee = Users.objects.create_user(
            username="empleado",
            email="empleado@test.com",
            password="Empleado123!",
            name="Empleado",
            company=self.company,
            role="employee",
            branch=self.branch
        )

        self.branch_stock = BranchStock.objects.create(
            branch=self.branch,
            product=self.product,
            current_stock=100
        )

        self.url = reverse('stock_movement-list')

    def test_admin_can_create_incoming_stock(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "movement_type": "incoming",
            "quantity": 50,
            "description": "Entrada de stock",
            "product": self.product.id,
            "branch": self.branch.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.branch_stock.refresh_from_db()
        self.assertEqual(self.branch_stock.current_stock, 150)

    def test_admin_cannot_create_zero_quantity(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "movement_type": "incoming",
            "quantity": 0,
            "description": "Cantidad cero",
            "product": self.product.id,
            "branch": self.branch.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_employee_cannot_move_stock_to_other_branch(self):
        other_branch = Branch.objects.create(
            company=self.company,
            name="Sucursal B",
            address="Calle Nueva",
            phone="222222222"
        )
        self.client.login(username="empleado", password="Empleado123!")
        data = {
            "movement_type": "incoming",
            "quantity": 10,
            "description": "Empleado intenta stock a otra sucursal",
            "product": self.product.id,
            "branch": other_branch.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_outgoing_stock_validation(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "movement_type": "outgoing",
            "quantity": 200,  # Más que el stock actual (100)
            "description": "Salida inválida",
            "product": self.product.id,
            "branch": self.branch.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_valid_outgoing_stock(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "movement_type": "outgoing",
            "quantity": 40,
            "description": "Salida válida",
            "product": self.product.id,
            "branch": self.branch.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.branch_stock.refresh_from_db()
        self.assertEqual(self.branch_stock.current_stock, 60)
