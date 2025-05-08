from rest_framework import serializers
from .models import *
from user_control.models import Users


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
    
    def validate_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo números. Ingrese un nombre válido.")
        return value
    
    def validate_cuit(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El cuit no puede contener letras.")
        return value
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El número no puede contener letras.")
        return value
    


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'phone']
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

    
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price']
        extra_kwargs = {
            'name': {'required': True},
            'category': {'required': True},
            'price': {'required': True},
        }
        
    def validate_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo números. Ingrese un nombre válido.")
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio no puede 0 o negativo.")
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        company = request.user.company
        name = attrs.get('name')

        # Excluir el producto actual (en caso de update)
        product_qs = Product.objects.filter(name__iexact=name, company=company)
        if self.instance:
            product_qs = product_qs.exclude(pk=self.instance.pk)

        if product_qs.exists():
            raise serializers.ValidationError({'name': 'Ya existe un producto con este nombre.'})
        
        return attrs


        
class BranchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchStock
        fields = '__all__'
        extra_kwargs = {
            'product': {'required': True},
            'branch': {'required': True},
        }
        
    def validate_current_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock actual no puede ser menor a 0.")
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            # Filtrar sucursales según el rol
            if request.user.role == 'admin':
                self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)
            elif request.user.role == 'employee':
                self.fields['branch'].queryset = Branch.objects.filter(pk=request.user.branch_id)
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)

    def validate(self, attrs):
        product = attrs.get('product')
        branch = attrs.get('branch')

        if not product or not branch:
            return attrs  # Evitar errores si aún no están definidos

        # Validar si ya existe esa combinación producto + sucursal
        qs = BranchStock.objects.filter(product=product, branch=branch)

        # Si estamos actualizando, excluimos este mismo objeto
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Este producto ya está registrado en esa sucursal.")

        return attrs


        
class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'movement_type', 'quantity', 'description', 'product', 'branch']
        
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock actual no puede ser menor a 0.")
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            # Filtrar sucursales según el rol
            if request.user.role == 'admin':
                self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)
            elif request.user.role == 'employee':
                self.fields['branch'].queryset = Branch.objects.filter(pk=request.user.branch_id)
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        movement_type = attrs.get('movement_type')
        branch = attrs.get('branch')
        product = attrs.get('product')

        if quantity == 0:
            raise serializers.ValidationError('No puede ingresar o sacar cantidad 0')

        # Validar si hay stock suficiente antes de restar
        if movement_type == 'outgoing':
            branch_stock = BranchStock.objects.filter(branch=branch, product=product).first()
            available = branch_stock.current_stock if branch_stock else 0
            if quantity > available:
                raise serializers.ValidationError(f'No hay stock suficiente. Disponible: {available}')

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        branch = validated_data['branch']
        product = validated_data['product']
        quantity = validated_data['quantity']
        movement_type = validated_data['movement_type']

        branch_stock, _ = BranchStock.objects.get_or_create(
            branch=branch,
            product=product,
            defaults={'current_stock': 0}
        )

        # Ya está validado que hay stock suficiente
        if movement_type == 'incoming':
            branch_stock.current_stock += quantity
        elif movement_type == 'outgoing':
            branch_stock.current_stock -= quantity

        branch_stock.save()

        return super().create(validated_data)
