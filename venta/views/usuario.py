from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Usuario

# utilities
from venta.serializers import UsuarioSerializer

# filters
from venta.filters import UsuarioFilter


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filterset_class = UsuarioFilter