from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuariosVistaViewSet,

)

router = DefaultRouter()
router.register(r'usuarios', UsuariosVistaViewSet, basename='usuarios')

urlpatterns = [
    path('user/', include(router.urls)),
]



