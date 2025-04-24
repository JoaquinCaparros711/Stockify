from rest_framework import serializers
from .models import Users
from control import models as control_model
from control import serializer as control_serializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    company = control_serializer.CompanySerializer(required=True)  # 🚀 Anidamos el CompanySerializer
    role = serializers.HiddenField(default='admin')

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'password2', 'name', 'role', 'company']
        extra_kwargs = {'email': {'required': True}}

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

    def create(self, validated_data):
        company = self.context['request'].user.company  # ✅ company del admin logueado
        branch = control_model.Branch.objects.create(company=company, **validated_data)
        return branch

