from django.shortcuts import render
from rest_framework import generics, viewsets

from .serializer import UsuarioSerializer
from django.contrib.auth.models import User

# Create your views here.
class UsuariosVistaViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    
    def perform_create(self, serializer):
        usuario = serializer.save()
        usuario.set_password(usuario.password)
        usuario.save()