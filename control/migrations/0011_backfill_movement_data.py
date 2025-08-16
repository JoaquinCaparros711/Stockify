from django.db import migrations

def forwards_func(apps, schema_editor):
    # Función para rellenar los datos históricos
    StockMovement = apps.get_model("control", "StockMovement")

    # Iteramos sobre todos los movimientos existentes
    for movement in StockMovement.objects.all():
        # Verificamos que las relaciones existan para evitar errores
        if movement.product:
            movement.product_name = movement.product.name
            movement.price_at_movement = movement.product.price
        else:
            movement.product_name = "Producto Eliminado"
            movement.price_at_movement = 0

        if movement.branch:
            movement.branch_name = movement.branch.name
        else:
            movement.branch_name = "Sucursal Eliminada"

        if movement.user:
            movement.user_name = movement.user.name # O .username, como prefieras
        else:
            movement.user_name = "Usuario Eliminado"

        movement.save()


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0010_stockmovement_branch_name_and_more'), # Reemplaza esto con el nombre de tu migración anterior
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]