from django.test import TestCase
from control.models import Company
from control.serializer import CompanySerializer
from rest_framework.exceptions import ValidationError


class CompanySerializerTests(TestCase):

    def test_valid_company_data(self):
        data = {
            "name": "Empresa SRL",
            "cuit": "20345678901",
            "email": "empresa@test.com",
            "phone": "2604000000",
            "address": "Calle Falsa 123"
        }
        serializer = CompanySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_name_cannot_be_only_numbers(self):
        data = {
            "name": "123456",
            "cuit": "20345678901",
            "email": "empresa@test.com",
            "phone": "2604000000",
            "address": "Calle Falsa 123"
        }
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"][0], "El nombre no puede ser solo números. Ingrese un nombre válido.")

    def test_cuit_must_be_digits_only(self):
        data = {
            "name": "Empresa Test",
            "cuit": "20A4567890X",
            "email": "empresa@test.com",
            "phone": "2604000000",
            "address": "Calle Falsa 123"
        }
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cuit", serializer.errors)
        self.assertEqual(serializer.errors["cuit"][0], "El cuit no puede contener letras.")

    def test_phone_must_be_digits_only(self):
        data = {
            "name": "Empresa Test",
            "cuit": "20345678901",
            "email": "empresa@test.com",
            "phone": "26ABC0000X",
            "address": "Calle Falsa 123"
        }
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)
        self.assertEqual(serializer.errors["phone"][0], "El número no puede contener letras.")

    def test_missing_required_fields(self):
        data = {}
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("cuit", serializer.errors)
        self.assertIn("email", serializer.errors)
