from django.contrib import admin
from .models import *

admin.site.register(Empresa)
admin.site.register(Sucursal)
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(StockSucursal)
admin.site.register(MovimientoStock)

