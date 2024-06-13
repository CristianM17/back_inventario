from django.contrib import admin
from django.urls import path
from .views import (
    ProductosAPIView,
    ListProductoListAPIView, 
    ModificarProductoRetrieveUpdateDestroyAPIView,
    IngresoMercanciAPIView,
    ActualizarIngresoMercanciAPIView,
    OrdenAPIView,
    VerFabricanteListAPIView,
    VerClienteListAPIView
)

urlpatterns = [
    path('productos/', ProductosAPIView.as_view()),
    path('lista-productos/', ListProductoListAPIView.as_view()),
    path('modificar-productos/<str:sku>/', ModificarProductoRetrieveUpdateDestroyAPIView.as_view()),
    path('ingreso-productos/', IngresoMercanciAPIView.as_view()),
    path('actualizar-ingreso-productos/<int:id>/', ActualizarIngresoMercanciAPIView.as_view()),
    path('crear-orden/', OrdenAPIView.as_view()),
    path('fabricantes/', VerFabricanteListAPIView.as_view()),
    path('clientes/', VerClienteListAPIView.as_view()),
]
