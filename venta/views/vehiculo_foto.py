from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import VehiculoFoto

# utilities
from venta.serializers import VehiculoFotoSerializer

# filters
from venta.filters import VehiculoFotoFilter


class VehiculoFotoViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = VehiculoFoto.objects.all()
    serializer_class = VehiculoFotoSerializer
    filterset_class = VehiculoFotoFilter