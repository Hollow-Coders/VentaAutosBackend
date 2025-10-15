from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Venta

# utilities
from venta.serializers import VentaSerializer

# filters
from venta.filters import VentaFilter


class VentaViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filterset_class = VentaFilter