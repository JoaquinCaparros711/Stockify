from rest_framework import serializers
from .models import Users
from control import models as control_model
from control import serializer as control_serializer
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    company = control_serializer.CompanySerializer(required=True)  
    role = serializers.HiddenField(default='admin')

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'name', 'role', 'company']
        extra_kwargs = {'email': {'required': True}, 'name': {'required': True}}
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un símbolo([!@#$%&*?).")
        return value
    
    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("El nombre no debe contener números.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        company_data = validated_data.pop('company')
        new_company = control_model.Company.objects.create(**company_data)
        validated_data['role'] = 'admin'

        user = Users.objects.create_user(company=new_company, **validated_data)
        return user

class UserCreateByAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un símbolo([!@#$%&*?).")
        return value
    
    def validate_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("El nombre no debe contener números.")
        return value

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'name', 'role', 'branch']
        extra_kwargs = {'email': {'required': True}}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 💡 Filtramos las sucursales según la empresa del usuario logueado
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = control_model.Branch.objects.filter(company=request.user.company)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})

        role = attrs.get('role')
        branch = attrs.get('branch')

        # Validar que empleados tengan una sucursal asignada
        if role == 'employee' and not branch:
            raise serializers.ValidationError({"branch": "Los empleados deben estar asignados a una sucursal."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        company = self.context['request'].user.company  # 🚀 El company del admin logueado
        user = Users.objects.create_user(company=company, **validated_data)
        return user


class BranchCreateByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = control_model.Branch
        fields = ['name', 'address', 'phone']
        extra_kwargs = {
            'name': {'required': True},
            'address': {'required': True},
            'phone': {'required': True},
        }
        
    def validate_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo números. Ingrese un nombre válido.")
        return value
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El número no puede contener letras.")
        return value

    def create(self, validated_data):
        company = self.context['request'].user.company  # ✅ company del admin logueado
        branch = control_model.Branch.objects.create(company=company, **validated_data)
        return branch

