from django.shortcuts import render

from rest_framework import viewsets

# models
from venta.models import Subasta

# utilities
from venta.serializers import SubastaSerializer

# filters
from venta.filters import SubastaFilter


class SubastaViewSet(viewsets.ModelViewSet):
    """
    View de Vehículos
    Maneja CRUD
    """
    queryset = Subasta.objects.all()
    serializer_class = SubastaSerializer
    filterset_class = SubastaFilter