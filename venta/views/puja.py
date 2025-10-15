from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Puja

# utilities
from venta.serializers import PujaSerializer

# filters
from venta.filters import PujaFilter


class PujaViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Puja.objects.all()
    serializer_class = PujaSerializer
    filterset_class = PujaFilter