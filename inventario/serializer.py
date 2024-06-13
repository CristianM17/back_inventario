from rest_framework import serializers
from .models import (
    Producto, 
    IngresoProducto,
    SalidaProducto, 
    Fabricante,
    Orden,
    OrdenProducto,
    Cliente,
    Seguimiento
)

from drf_extra_fields.fields import Base64ImageField

class FabricanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricante
        #fields = ['razon_social','nit']
        fields = '__all__'


class IngresoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoProducto
        fields = ['producto','cantidad']


class ProductoSerializer(serializers.ModelSerializer):
    imagen = Base64ImageField(required=False)
    
    class Meta:
        model = Producto
        fields = ['sku','nombre','imagen','descripcion','precio','stock_actual','fabricante','categoria','is_active']


class ListProductoSerializer(serializers.ModelSerializer):
    
    fabricante = FabricanteSerializer()
    
    class Meta:
        model = Producto
        exclude = ('fecha_creacion','fecha_actualizacion_stock',)


class OrdenSerializer(serializers.ModelSerializer):
    
    fecha_creacion_orden = serializers.DateField(required=False)
    
    class Meta:
        model = Orden
        fields = '__all__'
        

class OrdenProductoSerializer(serializers.ModelSerializer):
    orden = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = OrdenProducto
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cliente
        fields = '__all__'


class SalidaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalidaProducto
        exclude = ('fecha_salida',)


class CrearOrdenSerializer(serializers.Serializer):
    orden = OrdenSerializer()
    orden_producto = OrdenProductoSerializer(many=True)


class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        exclude = ('fecha_actualizacion_estado',)
