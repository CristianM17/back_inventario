from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError,APIException
from django.db import IntegrityError, transaction


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Producto,
    Fabricante,
    IngresoProducto,
    Orden,
    OrdenProducto,
    Seguimiento,
    SalidaProducto,
    Cliente
)

from .serializer import (
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


def respuestaCorrectaApis(object):
    respuesta = {
        "Error": "False",
        "Object": object
    }
    
    return respuesta


class ListProductoListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    #mirar si esto puede ser paginado
    queryset = Producto.objects.all()
    
    serializer_class = ListProductoSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'sku': ['contains'],
        'nombre': ['contains'],
        'categoria': ['contains']
    }
    search_fields = ['sku', 'nombre','categoria']
    ordering_fields = ['sku', 'nombre']
    ordering = ['sku']
    
    #metodo de ListApiview que se modifico para devolver la respuesta de forma diferente
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(respuestaCorrectaApis(serializer.data))


class ProductosAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
       serializador_producto = ProductoSerializer(data=request.data, many=True)
       
       try:
            if serializador_producto.is_valid(raise_exception=True):
                # Obtener los datos validados
                validated_data = serializador_producto.validated_data
                
                # Iterar sobre validated_data y agregarlos a una lista, se hace por el many=True
                lista_producto = []  
                for datos in validated_data:
                    #cambiar el nombre del archivo al del nombre del producto
                    nombre_archivo = datos['nombre']
                    nuevo_nombre = datos['imagen'].name

                    extension = nuevo_nombre[nuevo_nombre.index("."):]
                    nuevo_nombre = nombre_archivo + extension
                    datos['imagen'].name = nuevo_nombre
                          
                    #Guardar en base de datos      
                    producto = Producto(**datos)
                    producto.save()
                    lista_producto.append(ProductoSerializer(producto).data)
                
                return Response(respuestaCorrectaApis(lista_producto), status=status.HTTP_201_CREATED)
       except ValidationError:
            return Response(serializador_producto.errors, status=status.HTTP_400_BAD_REQUEST)


class ModificarProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'sku'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()        
        serializer = self.get_serializer(instance)
        
        if serializer.data['is_active']:
            custom_response = {
            "Error": "True",
            "Object": 'No se puede eliminar un producto que se encuentra activo'
        }
            raise APIException(custom_response)
        
        self.perform_destroy(instance)
        
        custom_response = {
            "descripcion": 'Producto eliminado correctamente'
        }
        
        return Response(respuestaCorrectaApis(custom_response), status=status.HTTP_204_NO_CONTENT)      


class IngresoMercanciAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
       serializador_ingreso = IngresoProductoSerializer(data=request.data, many=True)
       
       try:
            if serializador_ingreso.is_valid(raise_exception=True):
                # Obtener los datos validados
                validated_data = serializador_ingreso.validated_data
                
                lista_producto_ingresos = []  
                for ingresos in validated_data:
                    #Guardar en base de datos      
                    producto_ingresado = IngresoProducto(**ingresos)
                    producto_ingresado.save()
                    lista_producto_ingresos.append(IngresoProductoSerializer(producto_ingresado).data)
                
                return Response(respuestaCorrectaApis(lista_producto_ingresos), status=status.HTTP_201_CREATED)
       except ValidationError:
            return Response(serializador_ingreso.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ActualizarIngresoMercanciAPIView(APIView):
    permission_classes = [IsAuthenticated]
        
    def patch(self, request, *args, **kwargs):
        ingreso_producto = IngresoProducto.objects.filter(id=kwargs['id'])
        
        try:           
            if not ingreso_producto:
                custom_response = {
                    "Error": "True",
                    "Object": 'El id no se encuentra registrado'
                }
                raise ValidationError("No se encuentra id")
            
            ingreso_producto.update(cantidad=request.data['cantidad'])
        except ValidationError:
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)
        return Response(respuestaCorrectaApis({"id": kwargs['id'], "cantidad": request.data['cantidad']}), status=status.HTTP_201_CREATED)
               

class OrdenAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializador_crear_orden = CrearOrdenSerializer(data=request.data)
        
        try:
            with transaction.atomic():
                if serializador_crear_orden.is_valid(raise_exception=True):
                    data = serializador_crear_orden.data
                    #separar serializador para guardar los datos
                    serializador_orden = OrdenSerializer(data=data['orden'])
                    
                    if serializador_orden.is_valid(raise_exception=True):
                        orden = Orden(**serializador_orden.validated_data)
                        orden.save()
                          
                    lista_orden_productos = []  
                    for ordenes_productos in data['orden_producto']:
                        id_orden = {'orden': orden.id}
                        #añadir id_orden en el serializador
                        ordenes_productos.update(id_orden)
                        lista_orden_productos.append(ordenes_productos)     
                        
                    serializador_orden_producto = OrdenProductoSerializer(data=lista_orden_productos,many=True)
                        
                    if serializador_orden_producto.is_valid(raise_exception=True):
                            
                        for ordenes_productos_save in serializador_orden_producto.validated_data:  
                            orden_id = ordenes_productos_save.pop('orden')  
                            orden_instancia = Orden.objects.get(id=orden_id)
                            orden_producto = OrdenProducto(orden=orden_instancia, **ordenes_productos_save)
                            orden_producto.save()
                        
                    #Inserccion de datos en salida_productos
                    productos_orden = OrdenProducto.objects.filter(orden_id=orden_id)
                    
                    lista_salida_productos = []
                    for producto_salida in productos_orden:
                        stock = Producto.objects.get(sku=producto_salida.producto_sku_id)
                        if producto_salida.cantidad > stock.stock_actual:
                            raise IntegrityError(f"La cantidad del producto {stock.sku} para la orden es mayor a la cantidad en stock")
                        
                        data_salida = {
                            "producto": producto_salida.producto_sku_id,
                            "cantidad": producto_salida.cantidad,
                            "orden": orden_id
                        }
                        lista_salida_productos.append(data_salida)
                            
                            
                    serializador_salida_producto = SalidaProductoSerializer(data=lista_salida_productos,many=True)
                        
                    if serializador_salida_producto.is_valid(raise_exception=True):
                            
                        for salidas in serializador_salida_producto.validated_data:  
                            salida_producto = SalidaProducto(**salidas)
                            salida_producto.save()
                        
                    #Inserccion de datos en Seguimiento
                    data_seguimiento = {
                        "estado": 2,
                        "orden": orden_id
                    }
                    serializador_seguimiento = SeguimientoSerializer(data=data_seguimiento)
                        
                    if serializador_seguimiento.is_valid(raise_exception=True):  
                            seguimiento = Seguimiento(**serializador_seguimiento.validated_data)
                            seguimiento.save()  
                        
                    data_response = {
                        "id": orden_id,
                        "mensaje": "Se ha creado la orden exitosamente"
                    } 
                    
                return Response(respuestaCorrectaApis(data_response), status=status.HTTP_201_CREATED)
        except (IntegrityError, ValidationError) as e:
            return Response({e.args}, status=status.HTTP_400_BAD_REQUEST)


class VerFabricanteListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Fabricante.objects.all()
    serializer_class = FabricanteSerializer
    

class VerClienteListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer    