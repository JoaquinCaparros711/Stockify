from rest_framework import serializers
from .models import *
from user_control.models import Users


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
    
    

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price']

    def validate(self, attrs):
        request = self.context.get('request')
        company = request.user.company
        name = attrs.get('name')

        # Verifica si ya existe un producto con ese nombre para la misma empresa
        if Product.objects.filter(name__iexact=name, company=company).exists():
            raise serializers.ValidationError({'name': 'Ya existe un producto con este nombre.'})

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        company = request.user.company
        return Product.objects.create(company=company, **validated_data)

        
class BranchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchStock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)

    def validate(self, attrs):
        product = attrs.get('product')
        branch = attrs.get('branch')

        # Si se está creando (no actualizando)
        if self.instance is None:
            if BranchStock.objects.filter(product=product, branch=branch).exists():
                raise serializers.ValidationError("Este producto ya está registrado en esa sucursal.")

        return attrs

        
class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'description', 'product', 'branch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)

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
