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
    
    def test_employee_can_create_product(self):
        self.client.login(username="empleado", password="empleado123")

        url = reverse('product-list')
        data = {
            "name": "Producto creado por empleado",
            "description": "Valido",
            "category": "Categoria",
            "price": "100.00"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)  # ✅ Esperamos éxito
        self.assertTrue(Product.objects.filter(name="Producto creado por empleado").exists())
        
        
    def test_admin_cannot_delete_product_from_other_company(self):
        # Crear una empresa distinta
        other_company = Company.objects.create(
            name="Otra Empresa",
            cuit="99999999999",
            email="otra@empresa.com",
            phone="987654321",
            address="Calle Alternativa"
        )

        # Crear producto en esa otra empresa
        product = Product.objects.create(
            name="Producto de otra empresa",
            description="Test",
            category="X",
            price=100.0,
            company=other_company
        )

        # Crear otro admin de otra empresa
        another_admin = Users.objects.create_user(
            username="otroadmin",
            email="otroadmin@test.com",
            password="admin123",
            name="Otro Admin",
            company=self.company,  # Este admin sigue siendo de self.company
            role="admin"
        )

        self.client.login(username="otroadmin", password="admin123")

        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)  # No debería encontrarlo en el queryset
        self.assertTrue(Product.objects.filter(id=product.id).exists())
    
    def test_unauthenticated_user_cannot_create_product(self):
        self.client.logout()  # Asegura que no haya sesión activa

        data = {
            "name": "Producto sin login",
            "description": "Debe fallar",
            "category": "General",
            "price": "150.00"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    
