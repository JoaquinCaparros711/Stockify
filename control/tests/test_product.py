from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_control.models import Users
from control.models import Company, Product


class ProductValidationTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Empresa Test",
            cuit="12345678901",
            email="empresa@test.com",
            phone="1234567890",
            address="Calle Falsa 123"
        )
        self.admin = Users.objects.create_user(
            username="adminuser",
            email="admin@test.com",
            password="Admin123!",
            name="Administrador",
            company=self.company,
            role="admin"
        )
        self.client.login(username="adminuser", password="Admin123!")
        self.url = reverse('product-list')  # Asegúrate que tengas el router configurado

    def test_valid_product_creation(self):
        data = {
            "name": "Producto A",
            "description": "Desc A",
            "category": "Categoria A",
            "price": "100.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_name_with_only_numbers(self):
        data = {
            "name": "12345",
            "description": "Producto con número",
            "category": "General",
            "price": "100.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_price_zero(self):
        data = {
            "name": "Producto Barato",
            "description": "Precio cero",
            "category": "General",
            "price": "0"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_duplicate_product_name_same_company(self):
        # Crear producto original
        Product.objects.create(
            name="Producto Repetido",
            description="Original",
            category="General",
            price=100,
            company=self.company
        )
        # Intentar crear producto con el mismo nombre
        data = {
            "name": "Producto Repetido",
            "description": "Copia",
            "category": "General",
            "price": "200.00"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
    
    def test_employee_can_view_products_from_own_company(self):
        # Crear producto como admin
        product = Product.objects.create(
            company=self.company,
            name="Producto Admin",
            description="desc",
            category="cat",
            price=10.0
        )

        # Crear empleado de la misma empresa
        employee = Users.objects.create_user(
            username="empleado1",
            email="empleado1@test.com",
            password="Empleado123!",
            name="Empleado Uno",
            company=self.company,
            role="employee"
        )

        # Login como empleado
        self.client.login(username="empleado1", password="Empleado123!")

        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Producto Admin")
    
    def test_employee_cannot_create_product(self):
        self.client.login(username="empleado", password="empleado123")

        url = reverse('product-list')
        data = {
            "name": "Producto bloqueado",
            "description": "Intento de empleado",
            "category": "Prohibido",
            "price": "200.00"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)  # Esperamos 403 Forbidden
        self.assertFalse(Product.objects.filter(name="Producto bloqueado").exists())
        
        
    def test_admin_cannot_delete_product_from_other_company(self):
        self.client.login(username="otroadmin", password="admin123")

        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)  # 404 porque no está en el queryset
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())




    
