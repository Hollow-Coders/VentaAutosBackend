from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Modelo

# utilities
from venta.serializers import ModeloSerializer

# filters
from venta.filters import ModeloFilter


class ModeloViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    filterset_class = ModeloFilter