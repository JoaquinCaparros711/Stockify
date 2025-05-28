from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from control.models import Company
from user_control.models import Users


class UserSerializerTests(APITestCase):
    def setUp(self):
        self.create_url = reverse('admin-create-user')  # DRF router: user-list = POST/create

    def test_create_valid_user_and_company(self):
        self.client.logout()
        data = {
            "username": "joaco123",
            "email": "joaco@example.com",
            "password": "Password123!",
            "password2": "Password123!",
            "name": "Joaquin",
            "company": {
                "name": "Mi Empresa",
                "cuit": "12345678901",
                "email": "empresa@mail.com",
                "phone": "123456789",
                "address": "Av. Siempre Viva 123"
            }
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Users.objects.filter(username="joaco123").exists())

    def test_password_mismatch(self):
        self.client.logout()
        data = {
            "username": "joaco123",
            "email": "joaco@example.com",
            "password": "Password123!",
            "password2": "OtroPassword123!",
            "name": "Joaquin",
            "company": {
                "name": "Mi Empresa",
                "cuit": "12345678901",
                "email": "empresa@mail.com",
                "phone": "123456789",
                "address": "Av. Siempre Viva 123"
            }
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("password", response.data)

    def test_invalid_password_format(self):
        self.client.logout()
        data = {
            "username": "joaco123",
            "email": "joaco@example.com",
            "password": "password",
            "password2": "password",
            "name": "Joaquin",
            "company": {
                "name": "Mi Empresa",
                "cuit": "12345678901",
                "email": "empresa@mail.com",
                "phone": "123456789",
                "address": "Av. Siempre Viva 123"
            }
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("password", response.data)

    def test_name_with_numbers_invalid(self):
        self.client.logout()
        data = {
            "username": "joaco123",
            "email": "joaco@example.com",
            "password": "Password123!",
            "password2": "Password123!",
            "name": "Joaquin123",
            "company": {
                "name": "Mi Empresa",
                "cuit": "12345678901",
                "email": "empresa@mail.com",
                "phone": "123456789",
                "address": "Av. Siempre Viva 123"
            }
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("name", response.data)

    def test_authenticated_user_cannot_create_user(self):
        self.client.login(username='joaco', password='Admin123!')
        company = Company.objects.create(
            name="Empresa X",
            cuit="12345678901",
            email="empresa@x.com",
            phone="123456789",
            address="Calle Falsa 123"
        )
        Users.objects.create_user(
            username="admin",
            email="admin@x.com",
            password="Admin123!",
            name="Admin",
            company=company,
            role="admin"
        )
        self.client.login(username="admin", password="Admin123!")

        response = self.client.post(self.create_url, {
            "username": "nuevo",
            "email": "nuevo@x.com",
            "password": "Password123!",
            "password2": "Password123!",
            "name": "Nuevo",
            "company": {
                "name": "Otra",
                "cuit": "12345678999",
                "email": "otra@x.com",
                "phone": "987654321",
                "address": "Otra Calle"
            }
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("detail", response.data)
