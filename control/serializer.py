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

    # --- MÉTODO DE VALIDACIÓN AÑADIDO ---
    def validate(self, attrs):
        """
        Verifica que el nombre de la sucursal sea único para la compañía del usuario.
        """
        # Obtenemos el request del contexto para acceder al usuario logueado
        request = self.context.get('request')
        if not request or not hasattr(request, "user"):
            return attrs # No podemos validar si no tenemos el contexto del request

        company = request.user.company
        name = attrs.get('name')

        # Construimos la consulta para buscar duplicados (ignorando mayúsculas/minúsculas)
        queryset = Branch.objects.filter(company=company, name__iexact=name)

        # Si estamos actualizando (self.instance existe), debemos excluir
        # el objeto actual de la búsqueda. Esto permite guardar el formulario
        # sin cambiar el nombre, pero sin que dé un falso error de duplicado.
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        # Si la consulta encuentra algún resultado, significa que el nombre ya existe.
        if queryset.exists():
            # Lanzamos un error de validación que el front-end recibirá.
            raise serializers.ValidationError({
                'name': 'Ya existe una sucursal con este nombre en tu empresa.'
            })
            
        return attrs

    
    

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
    # Ya no necesitamos los 'source' porque ahora son campos del modelo.
    # Los definimos como read_only porque se calcularán automáticamente.
    user_name = serializers.CharField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    branch_name = serializers.CharField(read_only=True)
    price_at_movement = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = StockMovement
        # Añadimos el nuevo campo de precio
        fields = [
            'id', 'movement_type', 'quantity', 'description', 
            'product', 'branch', 'date', 'user', 
            'user_name', 'product_name', 'branch_name', 'price_at_movement'
        ]
        # Ya no es necesario 'write_only' en branch y user si los IDs son útiles en el frontend
        extra_kwargs = {
            'user': {'required': False} # El usuario se tomará del request
        }

    # Tus métodos __init__ y validate_quantity están bien.
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0.")
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'company'):
            if request.user.role == 'admin':
                self.fields['branch'].queryset = Branch.objects.filter(company=request.user.company)
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)
            elif request.user.role == 'employee':
                # Asegúrate que el empleado tenga un branch_id, si no, esto puede fallar.
                if request.user.branch_id:
                    self.fields['branch'].queryset = Branch.objects.filter(pk=request.user.branch_id)
                else:
                    self.fields['branch'].queryset = Branch.objects.none() # No puede seleccionar sucursal si no tiene una
                self.fields['product'].queryset = Product.objects.filter(company=request.user.company)

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        movement_type = attrs.get('movement_type')
        branch = attrs.get('branch')
        product = attrs.get('product')

        if quantity == 0:
            raise serializers.ValidationError('No puede ingresar o sacar cantidad 0')

        if movement_type == 'outgoing':
            branch_stock = BranchStock.objects.filter(branch=branch, product=product).first()
            available = branch_stock.current_stock if branch_stock else 0
            if quantity > available:
                raise serializers.ValidationError(f'No hay stock suficiente. Disponible: {available}')

        return attrs

    def create(self, validated_data):
        # --- LÓGICA DE "CONGELADO" DE DATOS ---
        # Obtenemos los objetos completos desde los datos validados
        product = validated_data.get('product')
        branch = validated_data.get('branch')
        user = self.context['request'].user # Obtenemos el usuario que hace la petición

        # Asignamos los datos "congelados" a los campos correspondientes
        validated_data['product_name'] = product.name
        validated_data['branch_name'] = branch.name
        validated_data['user_name'] = user.name  # O user.username, como prefieras
        validated_data['price_at_movement'] = product.price
        validated_data['user'] = user # Asignamos el usuario al ForeignKey

        # --- Lógica de actualización de stock (sin cambios) ---
        quantity = validated_data['quantity']
        movement_type = validated_data['movement_type']

        branch_stock, _ = BranchStock.objects.get_or_create(
            branch=branch, 
            product=product,
            defaults={'current_stock': 0}
        )

        if movement_type == 'incoming':
            branch_stock.current_stock += quantity
        elif movement_type == 'outgoing':
            if branch_stock.current_stock < quantity:
                raise serializers.ValidationError(f"Stock insuficiente para {product.name}. Disponible: {branch_stock.current_stock}")
            branch_stock.current_stock -= quantity

        branch_stock.save()

        return super().create(validated_data)