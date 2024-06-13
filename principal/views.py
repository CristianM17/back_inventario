from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Sum


from inventario.models import (
    Producto,
    Fabricante,
    IngresoProducto,
    Orden,
    OrdenProducto,
    Seguimiento,
    SalidaProducto,
    Cliente
)

from inventario.serializer import (
    IngresoProductoSerializer,
    ProductoSerializer,
    ListProductoSerializer, 
    CrearOrdenSerializer,
    OrdenSerializer,
    OrdenProductoSerializer,
    SalidaProductoSerializer,
    SeguimientoSerializer,
    FabricanteSerializer,
    ClienteSerializer
)

class ProductosBajoStockAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        #productos de bajo stock
        stock = Producto.objects.all().order_by('stock_actual')[:10]
        lista = []
        
        for bajo_stock in stock:
            dict_stock = {"producto": "", "cantidad": ""}            
            dict_stock['producto'] = bajo_stock.nombre
            dict_stock['cantidad'] = bajo_stock.stock_actual
            lista.append(dict_stock)
        
        dict_response = {"bajo_stock": lista, "productos_mas_vendidos": [], "inventario_por_categoria": []}
        
        #productos mas vendidos
        top_productos = SalidaProducto.objects.all().values('producto').annotate(cantidad=Sum('cantidad')).order_by('-cantidad')
        
        for top in top_productos:
           dict_response['productos_mas_vendidos'].append(top)
        
        #inventario por categoria
        categoria_productos = Producto.objects.all().values('categoria').annotate(stock_actual=Sum('stock_actual')).order_by('-stock_actual')
        
        for top in categoria_productos:
            for valor_categoria in categoria_productos.query.field.choices:
                if top['categoria'] == valor_categoria[0]:
                    top['categoria'] = f"{valor_categoria[0]} - {valor_categoria[1]}"
            
            dict_response['inventario_por_categoria'].append(top)
            
        return Response(dict_response)
        