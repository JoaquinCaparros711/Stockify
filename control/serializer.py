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
        fields = ['id', 'name', 'description', 'category', 'price']  # No incluir 'company' ni 'total_stock'

    def create(self, validated_data):
        request = self.context.get('request')
        company = request.user.company
        product = Product.objects.create(company=company, **validated_data)
        return product
        
class BranchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchStock
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)
        
class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'description', 'product', 'branch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user

        # Creamos el movimiento
        movement = super().create(validated_data)

        branch = movement.branch
        product = movement.product
        quantity = movement.quantity

        branch_stock, created = BranchStock.objects.get_or_create(
            branch=branch,
            product=product,
            defaults={'current_stock': 0}
        )

        if movement.movement_type == 'incoming':
            branch_stock.current_stock += quantity
        elif movement.movement_type == 'outgoing':
            if branch_stock.current_stock < quantity:
                raise serializers.ValidationError(f'No hay stock suficiente. Disponible: {branch_stock.current_stock}')
            branch_stock.current_stock -= quantity

        branch_stock.save()
        return movement