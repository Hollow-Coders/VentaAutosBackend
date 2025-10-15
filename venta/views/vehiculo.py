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


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filterset_class = VehiculoFilter

