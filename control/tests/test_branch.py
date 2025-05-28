
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_control.models import Users
from control.models import Company, Branch

class BranchSerializerTests(APITestCase):
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
        self.url = reverse('branch-list')

    def test_branch_list_accessible_by_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_branch_creation_not_allowed(self):
        # La vista no permite POST
        data = {
            "name": "Sucursal Nueva",
            "address": "Direccion 123",
            "phone": "1234567890"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_branch_name_only_numbers_invalid(self):
        branch = Branch.objects.create(name="Sucursal Valida", address="Test", phone="1234567890", company=self.company)
        url = reverse('branch-detail', args=[branch.id])
        data = {
            "name": "123456",
            "address": "Direccion Nueva",
            "phone": "1234567890"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_branch_phone_with_letters_invalid(self):
        branch = Branch.objects.create(name="Sucursal Valida", address="Test", phone="1234567890", company=self.company)
        url = reverse('branch-detail', args=[branch.id])
        data = {
            "name": "Sucursal Update",
            "address": "Nueva Direccion",
            "phone": "abc123"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)

    def test_branch_update_valid(self):
        branch = Branch.objects.create(name="Sucursal Update", address="Dir", phone="1234567890", company=self.company)
        url = reverse('branch-detail', args=[branch.id])
        data = {
            "name": "Sucursal Editada",
            "address": "Dir Actualizada",
            "phone": "9876543210"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Sucursal Editada")
