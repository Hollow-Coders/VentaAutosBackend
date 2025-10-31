from django.shortcuts import render

# Create your views here.
# models
from venta.models import Vehiculo
# rest
from rest_framework import viewsets
# utilities
from venta.serializers import VehiculoSerializer
# filters
from venta.filters import VehiculoFilter
# cosa para que funcionen los filtros?
from django_filters.rest_framework import DjangoFilterBackend


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filterset_class = VehiculoFilter
    filter_backends = [DjangoFilterBackend]

