from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Marca

# utilities
from venta.serializers import MarcaSerializer

# filters
from venta.filters import MarcaFilter


class MarcaViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    filterset_class = MarcaFilter