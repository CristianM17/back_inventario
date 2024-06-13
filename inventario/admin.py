from django.contrib import admin
from .models import (
Fabricante,Producto,Orden,Cliente,OrdenProducto,IngresoProducto,SalidaProducto,DevolucionProducto,Seguimiento
)

# Register your models here.
admin.site.register([Fabricante,Producto,Orden,Cliente,OrdenProducto,IngresoProducto,SalidaProducto,DevolucionProducto,Seguimiento])

