from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_control.models import Users
from control.models import Company, Branch, Product, BranchStock


class BranchStockTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Empresa X",
            cuit="12345678901",
            email="empresa@test.com",
            phone="123456789",
            address="Calle 123"
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
            description="Producto de prueba",
            category="General",
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

        self.url = reverse('branch_stock-list')

    def test_admin_can_create_branch_stock(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "product": self.product.id,
            "branch": self.branch.id,
            "current_stock": 50
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BranchStock.objects.count(), 1)

    def test_employee_can_create_stock_for_own_branch(self):
        self.client.login(username="empleado", password="Empleado123!")
        data = {
            "product": self.product.id,
            "branch": self.branch.id,
            "current_stock": 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_cannot_create_stock_for_other_branch(self):
        other_branch = Branch.objects.create(
            company=self.company,
            name="Sucursal B",
            address="Otra calle",
            phone="222222222"
        )
        self.client.login(username="empleado", password="Empleado123!")
        data = {
            "product": self.product.id,
            "branch": other_branch.id,
            "current_stock": 10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_prevent_duplicate_product_branch_combination(self):
        BranchStock.objects.create(product=self.product, branch=self.branch, current_stock=10)
        self.client.login(username="admin", password="Admin123!")
        data = {
            "product": self.product.id,
            "branch": self.branch.id,
            "current_stock": 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_stock_cannot_be_negative(self):
        self.client.login(username="admin", password="Admin123!")
        data = {
            "product": self.product.id,
            "branch": self.branch.id,
            "current_stock": -10
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_stock", response.data)
